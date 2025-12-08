# RAG Chatbot - Luật Bảo Hiểm Y Tế 🏥⚖️

Một ứng dụng chatbot AI thông minh được xây dựng với công nghệ **Retrieval-Augmented Generation (RAG)** để cung cấp tư vấn pháp lý về Luật Bảo hiểm y tế Việt Nam.

## 🎯 Tính Năng

- **Chatbot thông minh**: Trả lời các câu hỏi về Luật Bảo hiểm y tế
- **RAG (Retrieval-Augmented Generation)**: Kết hợp tìm kiếm vector và trí tuệ nhân tạo
- **Vector Database**: Sử dụng Pinecone để lưu trữ và tìm kiếm tài liệu
- **API RESTful**: Backend Flask với các endpoint API đầy đủ
- **Giao diện web hiện đại**: Frontend responsive với dark mode
- **Lịch sử chat**: Lưu trữ và quản lý các cuộc trò chuyện
- **Xử lý markdown**: Hỗ trợ định dạng văn bản rich text

## 📋 Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Node.js (optional, cho frontend development)
- Pinecone API Key
- Ollama (tùy chọn, nếu sử dụng local LLM)

## 🚀 Cài Đặt

### 1. Clone hoặc setup project

```bash
cd RAG/backend
```

### 2. Tạo virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment

Tạo file `.env` với các biến sau:

```env
PINECONE_API_KEY=your_pinecone_api_key_here

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

# Frontend Configuration
FRONTEND_API_URL=http://localhost:5000
```

## 💻 Chạy Ứng Dụng

### Backend API Server

```bash
cd backend
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

### Frontend

Mở file `frontend/index.html` trong trình duyệt hoặc sử dụng web server:

```bash
# Python 3
python -m http.server 8000 --directory frontend

# Hoặc sử dụng Node http-server
http-server frontend -p 8000
```

Frontend sẽ chạy tại: `http://localhost:8000`

## 📡 API Endpoints

### 1. Health Check

```
GET /api/health
```

Kiểm tra trạng thái của server và RAG system.

**Response:**
```json
{
  "status": "ok",
  "rag_initialized": true,
  "error": null
}
```

### 2. Initialize RAG System

```
POST /api/initialize
```

Khởi tạo hệ thống RAG (tạo vector database).

**Response:**
```json
{
  "status": "success",
  "message": "RAG system initialized successfully"
}
```

### 3. Chat (Main Endpoint)

```
POST /api/chat
```

Gửi câu hỏi và nhận phản hồi từ chatbot.

**Request Body:**
```json
{
  "question": "Luật Bảo hiểm y tế là gì?"
}
```

**Response:**
```json
{
  "status": "success",
  "question": "Luật Bảo hiểm y tế là gì?",
  "answer": "Luật Bảo hiểm y tế...",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 4. Get Specific Article

```
GET /api/articles/{article_number}
```

Lấy nội dung của một điều luật cụ thể.

**Example:** `GET /api/articles/1`

**Response:**
```json
{
  "status": "success",
  "article": 1,
  "content": "Điều 1: ..."
}
```

## 🛠️ Cấu Trúc Project

```
RAG/
├── backend/
│   ├── app.py              # Flask API server
│   ├── main.py             # Original console interface
│   ├── processing.py       # RAG logic
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables
│   └── data/
│       └── luatbhyt/      # Law documents
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── main.js            # API client & chat logic
│   ├── style.css          # Styling
│   └── jsonData.js        # Law data (reference)
└── README.md
```

## 🔧 Tối Ưu Hóa Hiệu Suất

### Frontend

- **Lazy Loading**: Chat history được tải theo yêu cầu
- **Local Storage**: Lưu trữ history cuc bộ để tránh yêu cầu API
- **Debouncing**: Tránh gửi requests liên tiếp
- **Code Splitting**: Chia nhỏ JavaScript code

### Backend

- **Caching**: Lưu vector embeddings
- **Connection Pooling**: Tối ưu kết nối Pinecone
- **Async Processing**: Xử lý requests không đồng bộ (tùy chọn)

## 🐛 Troubleshooting

### "Connection refused" Error

```
❌ Lỗi kết nối: [Errno 111] Connection refused
```

**Giải pháp:**
- Kiểm tra backend server có đang chạy không
- Kiểm tra FLASK_PORT trong .env
- Kiểm tra FRONTEND_API_URL trong HTML

### "Pinecone API Key Error"

```
Error: Invalid Pinecone API Key
```

**Giải pháp:**
- Kiểm tra PINECONE_API_KEY trong .env
- Đảm bảo API key không có khoảng trắng
- Tạo API key mới từ Pinecone dashboard

### "VectorDB Not Initialized"

```
RAG system not initialized
```

**Giải pháp:**
- Gọi endpoint `/api/initialize` trước
- Kiểm tra file dữ liệu trong `data/luatbhyt/`
- Xem logs để xác định vấn đề cụ thể

## 📚 Hướng Dẫn Sử Dụng

### Cho Người Dùng

1. **Mở ứng dụng**: Truy cập `http://localhost:8000`
2. **Đợi khởi tạo**: Hệ thống sẽ tự động khởi tạo RAG
3. **Đặt câu hỏi**: Nhập câu hỏi và nhấn Enter hoặc click nút gửi
4. **Xem lịch sử**: Nhấp vào các cuộc trò chuyện trước trong sidebar
5. **Dark Mode**: Sử dụng nút 🌙 để bật/tắt dark mode

### Cho Nhà Phát Triển

#### Thêm Endpoint Mới

```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    # Xử lý logic
    return jsonify({'status': 'success', 'data': result})
```

#### Mở Rộng Frontend

```javascript
// Thêm event listener mới
document.addEventListener('customEvent', () => {
    // Handle event
});

// Thêm API call mới
async function newApiCall() {
    const response = await fetch(`${API_BASE_URL}/new-endpoint`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: value})
    });
    return response.json();
}
```

## 🔐 Security Best Practices

1. **Không commit .env**: Thêm .env vào .gitignore
2. **Rate Limiting**: Thêm rate limiting cho API (tùy chọn)
3. **Input Validation**: Luôn validate input từ user
4. **CORS**: Cấu hình CORS cho production
5. **HTTPS**: Sử dụng HTTPS cho production

```python
# Production CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

## 🧪 Testing

### Test Backend

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Luật Bảo hiểm y tế là gì?"}'
```

### Test Frontend

Sử dụng browser DevTools:

```javascript
// Kiểm tra API connection
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(console.log)
```

## 📈 Scaling

### Multi-Worker Setup (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📝 Changelog

### v1.0.0 (2024-01-01)
- ✅ Frontend & Backend API integration hoàn chỉnh
- ✅ RAG system hoạt động
- ✅ Chat history management
- ✅ Dark mode support
- ✅ Markdown formatting

## 🤝 Đóng Góp

Những cải tiến được đề xuất:

1. Thêm streaming response
2. Multi-language support
3. Admin dashboard
4. User authentication
5. Feedback system
6. Export chat history

## 📄 License

Project này được phát triển cho mục đích giáo dục.

## 📞 Support

Để báo cáo lỗi hoặc yêu cầu hỗ trợ, vui lòng tạo issue hoặc liên hệ trực tiếp.

---

**Happy Chatting!** 🚀
