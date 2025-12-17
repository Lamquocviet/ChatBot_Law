# 🚀 QUICK START GUIDE - RAG Chatbot Setup

Hướng dẫn nhanh để khởi chạy RAG Chatbot trong 5 phút!

## 1️⃣ Chuẩn Bị (Preparation)

### Bước 1: Kiểm Tra Python
```bash
python --version
# Cần Python 3.8 trở lên
```

### Bước 2: Lấy Pinecone API Key
1. Truy cập https://www.pinecone.io/
2. Đăng ký hoặc đăng nhập
3. Tạo API Key từ dashboard
4. Copy API key

## 2️⃣ Cài Đặt Backend (3 phút)

### Bước 1: Mở Terminal trong thư mục backend
```bash
cd RAG/backend
```

### Bước 2: Tạo Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Tạo .env File
Tạo file `.env` trong thư mục `backend/` với nội dung:
```env
PINECONE_API_KEY=your_api_key_here
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False
FRONTEND_API_URL=http://localhost:5000
```

### Bước 5: Chạy Backend
```bash
python app.py
```

✅ Backend đang chạy tại: `http://localhost:5000`

## 3️⃣ Chạy Frontend (30 giây)

### Cách 1: Sử dụng Python
```bash
# Từ thư mục frontend/
cd ../frontend
python -m http.server 8000
```

### Cách 2: Sử dụng Node.js
```bash
npx http-server frontend -p 8000
```

### Cách 3: Mở File Trực Tiếp
Đơn giản mở `frontend/index.html` bằng trình duyệt

✅ Frontend chạy tại: `http://localhost:8000`

## 4️⃣ Kiểm Tra Hoạt động (Testing)

### Bước 1: Kiểm Tra Backend
```bash
curl http://localhost:5000/api/health
```

**Kết quả mong đợi:**
```json
{
  "status": "ok",
  "rag_initialized": false,
  "error": null
}
```

### Bước 2: Mở Frontend
Truy cập `http://localhost:8000` trong trình duyệt

### Bước 3: Đợi Khởi Tạo
- Trang sẽ hiển thị "✓ 系统已就绪" khi RAG được khởi tạo
- **Lưu ý:** Lần đầu có thể mất 30-60 giây

### Bước 4: Đặt Câu Hỏi
Nhập: "Luật Bảo hiểm y tế là gì?"

**Kết quả:** Bạn sẽ nhận được câu trả lời từ AI

## 🎯 Điều Gì Vừa Được Setup?

### Backend (Flask API Server)
```
/api/health          → Kiểm tra trạng thái
/api/initialize      → Khởi tạo RAG system
/api/chat            → Gửi câu hỏi & nhận phản hồi
/api/articles/{id}   → Lấy điều luật cụ thể
```

### Frontend (Web Interface)
```
✅ Chat interface
✅ Chat history sidebar
✅ Dark mode toggle
✅ Message formatting
✅ Loading indicators
✅ Error handling
```

### Backend Features (RAG System)
```
✅ Vector database (Pinecone)
✅ Embedding models
✅ LLM integration (Ollama)
✅ Chat context management
```

## 🐛 Troubleshooting Nhanh

### ❌ "Connection refused"
```bash
# Kiểm tra backend có chạy không
curl http://localhost:5000/api/health

# Nếu không, chạy lại:
python app.py
```

### ❌ "Pinecone API Key error"
1. Mở `.env`
2. Kiểm tra API key không có space
3. Tạo API key mới từ Pinecone

### ❌ "RAG not initialized"
1. Refresh trang web
2. Chờ 30-60 giây để khởi tạo
3. Kiểm tra console (F12) xem có error không

### ❌ "Empty response"
- Kiểm tra file data trong `backend/data/luatbhyt/`
- Đảm bảo có file `law.txt`

## 📝 Commands Tóm Tắt

```bash
# Terminal 1: Backend
cd RAG/backend
python -m venv venv
venv\Scripts\activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2: Frontend
cd RAG/frontend
python -m http.server 8000
```

## 🔧 Development Tips

### Hot Reload Backend
Thay đổi `FLASK_DEBUG=True` trong `.env`

### Xóa Cache
```bash
# Xóa __pycache__
rmdir /s __pycache__

# Xóa localStorage (trong DevTools)
localStorage.clear()
```

### View API Requests
Mở DevTools (F12) → Network tab → Chat

## ✅ Checklist Hoàn Thiện

- [ ] Python 3.8+ được cài đặt
- [ ] Pinecone API Key được lấy
- [ ] .env file được tạo với API key
- [ ] Backend dependencies được cài (pip install -r requirements.txt)
- [ ] Backend chạy thành công (python app.py)
- [ ] Frontend có thể truy cập (http://localhost:8000)
- [ ] Health check trả về "ok"
- [ ] RAG system được khởi tạo
- [ ] Có thể gửi chat message
- [ ] Nhận được phản hồi từ AI

## 🎓 Học Thêm

### File Chính:
- `backend/app.py` - Flask API server
- `backend/processing.py` - RAG logic
- `frontend/main.js` - Chat client
- `frontend/index.html` - UI layout
- `frontend/style.css` - Styling

### Tiếp Theo:
1. Đọc README.md chi tiết
2. Xem API documentation
3. Tùy chỉnh styling/features
4. Deploy lên server

## 🚀 Next Steps

### Development:
```bash
# Thêm new API endpoint
# Chỉnh sửa AI prompt
# Tùy chỉnh styling
# Thêm features mới
```

### Production:
```bash
# Set FLASK_DEBUG=False
# Sử dụng Gunicorn/uWSGI
# Thêm authentication
# Setup HTTPS
# Deploy lên cloud
```

## 💡 Pro Tips

1. **Keyboard Shortcut**: Shift+Enter để gửi (có thể config)
2. **Dark Mode**: Bật tự động nếu OS dùng dark mode
3. **Export Chat**: Save chat history as JSON
4. **Custom Prompt**: Chỉnh sửa system prompt trong `processing.py`

## 📞 Cần Giúp?

1. Kiểm tra logs trong terminal
2. Xem DevTools Console (F12)
3. Đọc error messages kỹ
4. Restart tất cả services

---

**Chúc mừng! Ứng dụng của bạn đã sẵn sàng!** 🎉

Bây giờ bạn có thể:
- 💬 Chat với AI
- 📚 Hỏi về luật
- 💾 Lưu history
- 🌙 Sử dụng dark mode
- 🔗 Tương tác với backend API

**Happy Coding!** 🚀
