from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import os
import re
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import warnings
warnings.filterwarnings('ignore')

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


class RAG:
    def __init__(self, data_folder="data/luatbhyt"):
        print("[DEBUG] Khởi tạo RAG...")

        self.data_folder = data_folder
        print("[DEBUG] Load model embedding...")
        self.vector_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.pinecone = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = "my-vector-db"

        print("[DEBUG] Kiểm tra index Pinecone...")
        if self.index_name not in self.pinecone.list_indexes().names():
            print("[DEBUG] Index chưa có → tạo mới...")
            self.pinecone.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        else:
            print("[DEBUG] Index đã tồn tại.")

        self.index = self.pinecone.Index(self.index_name)
        print("[DEBUG] Kết nối Pinecone OK.")

        self.context = []

        # HTTP session reused for model requests (connection pooling + retries)
        self.http = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=(500, 502, 504))
        adapter = HTTPAdapter(max_retries=retries)
        self.http.mount("http://", adapter)
        self.http.mount("https://", adapter)

        # Simple in-memory LRU cache for query embeddings/results
        self._embed_cache = OrderedDict()
        self._embed_cache_max = 128
        # Simple in-memory LRU cache for full query -> response
        self._response_cache = OrderedDict()
        self._response_cache_max = 256

        # Load law text once to speed up raw article search
        law_path = os.path.join(self.data_folder, "law.txt")
        self._law_text = None
        if os.path.exists(law_path):
            try:
                with open(law_path, "r", encoding="utf-8") as f:
                    self._law_text = f.read().lower()
            except Exception:
                self._law_text = None
        # Load QA pairs
        qa_path = os.path.join(self.data_folder, "qa.txt")
        self._qa_pairs = []
        if os.path.exists(qa_path):
            try:
                with open(qa_path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()

                q, a = None, None
                for line in lines:
                    if line.startswith("Q:"):
                        q = line[2:].strip()
                    elif line.startswith("A:") and q:
                        a = line[2:].strip()
                        self._qa_pairs.append((q, a))
                        q, a = None, None
            except Exception:
                self._qa_pairs = []
        #load concepts
        # Load concepts (K:)
        concepts_path = os.path.join(self.data_folder, "concepts.txt")
        self._concepts = {}

        if os.path.exists(concepts_path):
            try:
                with open(concepts_path, "r", encoding="utf-8") as f:
                    blocks = f.read().split("\n\n")

                for block in blocks:
                    lines = block.strip().splitlines()
                    if len(lines) >= 2 and lines[0].lower().startswith("k:"):
                        key = lines[0][2:].strip().lower()
                        value = " ".join(lines[1:]).strip()
                        self._concepts[key] = value
            except Exception:
                self._concepts = {}

        


    # ======================
    #    TÌM ĐIỀU LUẬT RAW
    # ======================
    def search_raw_article(self, query):
        q_norm = query.lower().strip()
        # ======================
        # 0. ƯU TIÊN ĐỊNH NGHĨA (K:)
        # ======================
        if q_norm.startswith("k:"):
            term = q_norm[2:].strip()
            for key, value in self._concepts.items():
                if term in key:
                    print("[DEBUG] Trả lời từ concepts.txt")
                    return value
            return "Không tìm thấy định nghĩa phù hợp trong Luật BHYT."
        # ======================
        # 1. ƯU TIÊN Q&A
        # ======================
        if q_norm.startswith("q:"):
            q_norm = q_norm[2:].strip()

        for q, a in self._qa_pairs:
            if q.lower().strip() == q_norm:
                print("[DEBUG] Trả lời từ QA.txt (không RAG)")
                return a

        # ======================
        # 2. TÌM ĐIỀU LUẬT RAW
        # ======================
        print("[DEBUG] Kiểm tra yêu cầu có chứa 'Điều X' hay không...")

        match = re.search(r"điều\s+(\d+)", q_norm)
        if not match:
            return None

        article_number = int(match.group(1))
        target = f"điều {article_number}"

        full_text = self._law_text
        if not full_text:
            return None

        idx = full_text.find(target)
        if idx == -1:
            return None

        next_match = re.search(rf"điều\s+{article_number + 1}\b", full_text[idx:])
        end = idx + next_match.start() if next_match else idx + 2500

        print("[DEBUG] Trả về Điều luật raw")
        return full_text[idx:end].strip()

        


    # ======================
    #      Đọc file TXT
    # ======================
    def read_text(self, filepath):
        print(f"[DEBUG] Đọc file: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        print(f"[DEBUG] Độ dài văn bản: {len(text)} ký tự")
        return text, os.path.basename(filepath)


    # ======================
    #    Chunk văn bản
    # ======================
    def text_to_docs(self, text, filename):
        print(f"[DEBUG] Chia chunk cho file: {filename}")

        if isinstance(text, str):
            text = [text]

        page_docs = [Document(page_content=page) for page in text]
        for i, doc in enumerate(page_docs):
            doc.metadata["page"] = i + 1

        doc_chunks = []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )

        for doc in page_docs:
            chunks = splitter.split_text(doc.page_content)
            print(f"[DEBUG] Tổng chunk tạo ra: {len(chunks)}")

            for i, chunk in enumerate(chunks):
                new_doc = Document(
                    page_content=chunk,
                    metadata={
                        "page": doc.metadata["page"],
                        "chunk": i,
                        "filename": filename
                    }
                )
                new_doc.metadata["source"] = f"{new_doc.metadata['page']}-{new_doc.metadata['chunk']}"
                doc_chunks.append(new_doc)

        return doc_chunks


    # ======================
    #    Index Pinecone
    # ======================
    def docs_to_index(self, docs):
        print(f"[DEBUG] Bắt đầu index {len(docs)} chunk...")
        batch = []
        batch_size = 50
        for i, doc in enumerate(docs):
            if i % 100 == 0:
                print(f"[DEBUG] ...indexing chunk {i}/{len(docs)}")

            embedding = self.vector_model.encode([doc.page_content])[0].tolist()

            metadata = {
                "page": doc.metadata["page"],
                "chunk": doc.metadata["chunk"],
                "filename": doc.metadata["filename"],
                "text": doc.page_content,
            }

            batch.append((doc.metadata["source"], embedding, metadata))

            if len(batch) >= batch_size:
                self.index.upsert(vectors=batch)
                batch = []

        if batch:
            self.index.upsert(vectors=batch)

        print("[DEBUG] Indexing hoàn tất!")


    # ======================
    #    Tạo vector DB
    # ======================
    def create_vectordb(self):
        print("[DEBUG] Tạo vector DB từ thư mục:", self.data_folder)
        documents = []

        for file in os.listdir(self.data_folder):
            if file.endswith(".txt"):
                print(f"[DEBUG] → Xử lý file: {file}")
                full_path = os.path.join(self.data_folder, file)
                text, filename = self.read_text(full_path)
                docs = self.text_to_docs(text, filename)
                documents.extend(docs)

        print(f"[DEBUG] Tổng số doc chunk: {len(documents)}")
        self.docs_to_index(documents)


    # ======================
    #       Truy vấn
    # ======================
    def retrieve_relevant_docs(self, query, top_k=3, threshold=0.35):
        print(f"[DEBUG] Truy vấn: {query}")
        # Use simple LRU cache for embeddings to avoid recomputing identical queries
        if query in self._embed_cache:
            embedding = self._embed_cache.pop(query)
            # move to end to mark as most recently used
            self._embed_cache[query] = embedding
        else:
            embedding = self.vector_model.encode([query])[0].tolist()
            self._embed_cache[query] = embedding
            if len(self._embed_cache) > self._embed_cache_max:
                self._embed_cache.popitem(last=False)

        res = self.index.query(vector=embedding, top_k=top_k, include_metadata=True)

        print("[DEBUG] Kết quả top-k:", len(res["matches"]))

        matches = [m for m in res["matches"] if m["score"] >= threshold]
        print(f"[DEBUG] Sau threshold {threshold}: còn {len(matches)} kết quả")

        return matches


    # ======================
    #      Generate answer
    # ======================
    def generate_response(self, query):
        print("[DEBUG] Gọi generate_response()")

        # ƯU TIÊN trả về raw Điều X
        raw_article = self.search_raw_article(query)
        if raw_article:
            return raw_article

        # Ngược lại → dùng RAG
        # Check response cache first to return instantly for repeated queries
        if query in self._response_cache:
            resp = self._response_cache.pop(query)
            # mark as recently used
            self._response_cache[query] = resp
            print("[DEBUG] Trả về từ response cache")
            return resp

        docs = self.retrieve_relevant_docs(query)

        # If top match is very confident, return the source text directly
        if docs and len(docs) > 0 and docs[0].get("score", 0) >= 0.82:
            print("[DEBUG] High-confidence match found — returning source snippet without calling LLM")
            return docs[0]["metadata"]["text"]
        # Join only top docs' text and truncate to a reasonable size to
        # avoid sending huge payloads to the model which slows responses.
        context = " ".join([d["metadata"]["text"] for d in docs[:5]])
        max_context_chars = 3500
        if len(context) > max_context_chars:
            context = context[-max_context_chars:]

        print(f"[DEBUG] Độ dài context gửi vào model: {len(context)}")

        input_text = f"""
            Bạn là chuyên gia rất am hiểu về Luật BHYT. Dựa trên Ngữ cảnh được cung cấp bên dưới, trả lời câu hỏi một cách thật chính xác và ngắn gọn.
            BẮT BUỘC phải trích dẫn điều luật chính xác nếu có trong ngữ cảnh (Không được sai sót về số điều luật). 
            Ngữ cảnh: {context}
            Câu hỏi: {query}
        """

        payload = {
            "model": "llama3.1",
            "prompt": input_text,
            "context": self.context,
            "stream": False,
        }

        print(f"[DEBUG] Gửi request tới Ollama...")
        response = self.http.post(url="http://localhost:11434/api/generate", json=payload)
        response = response.json()

        print("[DEBUG] Nhận phản hồi từ model!")

        self.context = response.get("context", self.context)
        answer = response.get("response") or response.get("output") or ""

        # Save to response cache
        try:
            self._response_cache[query] = answer
            if len(self._response_cache) > self._response_cache_max:
                self._response_cache.popitem(last=False)
        except Exception:
            pass

        return answer
