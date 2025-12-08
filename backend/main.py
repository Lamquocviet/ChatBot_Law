from processing import RAG

rag = RAG()

print("[DEBUG] Bắt đầu tạo VectorDB...")
rag.create_vectordb()
print("[DEBUG] VectorDB đã sẵn sàng!\n")

while True:
    try:
        user_input = input("Người dùng: ")
        if user_input.strip().lower() == "end":
            break

        response = rag.generate_response(user_input)
        print("CHATBOT:", response)
        print()

    except KeyboardInterrupt:
        break
