# Troubleshooting & FAQ

## Quick Troubleshooting

| Problem | Solution | More Info |
|---------|----------|-----------|
| Backend won't start | Check Python version, pip install packages | [Setup Issues](#setup-issues) |
| Frontend can't connect | Backend not running, wrong API URL | [Connection Issues](#connection-issues) |
| "API Key error" | Wrong Pinecone key, check .env file | [Configuration Issues](#configuration-issues) |
| Messages not showing | Check browser console (F12) | [Frontend Issues](#frontend-issues) |
| Slow responses | RAG initializing, Ollama needs time | [Performance Issues](#performance-issues) |

---

## Setup Issues

### Problem: `ModuleNotFoundError: No module named 'flask'`

**Symptoms:**
```
Traceback (most recent call last):
  File "app.py", line 1, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**

1. **Check virtual environment is activated:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
   
   You should see `(venv)` in your terminal prompt.

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import flask; print(flask.__version__)"
   ```

**Prevention:**
- Always activate venv before working
- Double-check all dependencies are installed

---

### Problem: `Python version not supported`

**Symptoms:**
```
ERROR: Python 3.7 is not supported by this version
```

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version
   ```

2. **Need Python 3.8+:**
   - Download from https://www.python.org/
   - Make sure to add to PATH during installation

3. **If multiple versions installed:**
   ```bash
   python3.11 -m pip install -r requirements.txt
   ```

**Prevention:**
- Always use Python 3.8+
- Keep Python updated

---

### Problem: `pip install fails with SSL error`

**Symptoms:**
```
ERROR: Could not fetch URL... SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**

1. **Disable SSL verification (temporary):**
   ```bash
   pip install --trusted-host pypi.python.org -r requirements.txt
   ```

2. **Use official Python installer** (includes SSL certificates)

3. **Update pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

**Prevention:**
- Use official Python installer
- Keep SSL certificates updated

---

## Connection Issues

### Problem: `Connection refused` when accessing backend

**Symptoms:**
```
❌ Lỗi kết nối: [Errno 111] Connection refused
```

**Solutions:**

1. **Verify backend is running:**
   ```bash
   # In another terminal
   curl http://localhost:5000/api/health
   ```

2. **Check port is correct:**
   - Frontend should use: `http://localhost:5000`
   - Check .env has `FLASK_PORT=5000`

3. **If port in use:**
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -i :5000
   kill -9 <PID>
   ```

4. **Try different port:**
   - Change FLASK_PORT in .env
   - Update FRONTEND_API_URL accordingly
   - Restart backend

**Prevention:**
- Keep terminal with backend running visible
- Note the port being used

---

### Problem: `CORS error` in browser console

**Symptoms:**
```
Access to XMLHttpRequest at 'http://localhost:5000/api/chat'
from origin 'http://localhost:8000' has been blocked by CORS policy
```

**Solutions:**

1. **Check backend has CORS enabled:**
   ```python
   # In app.py, should have:
   from flask_cors import CORS
   CORS(app)
   ```

2. **Verify in console:**
   ```javascript
   // In browser console
   fetch('http://localhost:5000/api/health')
     .then(r => r.json())
     .then(console.log)
   ```

3. **If still failing:**
   - Make sure `flask-cors` is installed
   - Restart backend server
   - Hard refresh browser (Ctrl+Shift+R)

**Prevention:**
- Ensure CORS is imported and initialized
- Test API connection early

---

## Configuration Issues

### Problem: `Pinecone API Key error`

**Symptoms:**
```
Error: Invalid Pinecone API Key
Error initializing RAG: Authentication failed
```

**Solutions:**

1. **Verify API key format:**
   - Should start with `pcsk_`
   - Should be long string (50+ characters)

2. **Check .env file:**
   ```bash
   cat .env | grep PINECONE
   # Or on Windows
   type .env | findstr PINECONE
   ```

3. **No spaces in key:**
   ```env
   # ✅ Correct
   PINECONE_API_KEY=pcsk_xxxxx
   
   # ❌ Wrong
   PINECONE_API_KEY = pcsk_xxxxx
   PINECONE_API_KEY=pcsk_xxxxx 
   ```

4. **Generate new key:**
   - Visit https://www.pinecone.io/
   - Login to dashboard
   - Create new API key
   - Copy and paste carefully

5. **Restart backend:**
   ```bash
   # Press Ctrl+C to stop
   # Then start again
   python app.py
   ```

**Prevention:**
- Copy-paste API keys carefully
- Don't add extra spaces
- Use `.env` file instead of hardcoding

---

### Problem: `.env file not found`

**Symptoms:**
```
Error: [Errno 2] No such file or directory: '.env'
KeyError: 'PINECONE_API_KEY'
```

**Solutions:**

1. **Create .env file:**
   ```bash
   # Navigate to backend directory
   cd backend
   
   # Create file
   # Windows (PowerShell)
   New-Item -Name ".env" -ItemType "file"
   
   # Linux/Mac
   touch .env
   ```

2. **Add content to .env:**
   ```env
   PINECONE_API_KEY=your_key_here
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   FLASK_DEBUG=False
   FRONTEND_API_URL=http://localhost:5000
   ```

3. **Verify file location:**
   ```bash
   # Should be in backend/ directory
   ls -la .env      # Linux/Mac
   dir .env         # Windows
   ```

**Prevention:**
- Always create .env in backend directory
- Don't use .env.txt (must be just .env)
- Save with UTF-8 encoding

---

## Frontend Issues

### Problem: `API_BASE_URL is not defined`

**Symptoms:**
```
Uncaught ReferenceError: API_BASE_URL is not defined
```

**Solutions:**

1. **Check main.js is loaded:**
   ```html
   <!-- In index.html, should have -->
   <script src="/static/main.js"></script>
   <!-- OR -->
   <script src="main.js"></script>
   ```

2. **Verify API_BASE_URL is defined:**
   ```javascript
   // In main.js, should have at top:
   const API_BASE_URL = 'http://localhost:5000/api';
   ```

3. **Check console for errors:**
   - Open DevTools (F12)
   - Go to Console tab
   - Look for red errors
   - Check Network tab for 404 on main.js

4. **Reload page:**
   - Hard refresh: Ctrl+Shift+R
   - Clear cache if needed

**Prevention:**
- Check main.js loads successfully (Network tab)
- Verify script tags in HTML
- Test API_BASE_URL in console

---

### Problem: `localStorage not working`

**Symptoms:**
```
Chat history not saving
Messages disappear after refresh
```

**Solutions:**

1. **Check if localStorage is enabled:**
   ```javascript
   // In browser console:
   localStorage.setItem('test', 'value');
   localStorage.getItem('test');
   ```

2. **Clear localStorage:**
   ```javascript
   // In browser console:
   localStorage.clear();
   ```

3. **Check browser settings:**
   - Some browsers disable localStorage in private mode
   - Check if site is allowed to store data
   - Increase storage quota if needed

4. **Check for errors:**
   - Open DevTools (F12)
   - Go to Console tab
   - Look for storage errors

**Prevention:**
- Test localStorage early
- Handle quota exceeded errors
- Use private/incognito only for testing

---

### Problem: `Dark mode not working`

**Symptoms:**
```
Dark mode button does nothing
Class 'dark-mode' not applied
```

**Solutions:**

1. **Check toggleDarkMode function:**
   ```javascript
   // Should be in main.js
   function toggleDarkMode() {
       isDarkMode = !isDarkMode;
       document.body.classList.toggle('dark-mode');
       localStorage.setItem(DARK_MODE_STORAGE_KEY, isDarkMode);
   }
   ```

2. **Check CSS for dark mode:**
   ```css
   /* In style.css, should have */
   body.dark-mode {
       --bg-light: #1a1a1a;
       /* ... more variables */
   }
   ```

3. **Verify button calls function:**
   ```html
   <!-- In index.html -->
   <button onclick="toggleDarkMode()">🌙 Dark Mode</button>
   ```

4. **Hard refresh:**
   - Clear cache: Ctrl+Shift+Delete
   - Reload page: Ctrl+Shift+R

**Prevention:**
- Test dark mode early
- Check browser DevTools for CSS errors
- Verify classes are applied in Elements tab

---

## Backend Issues

### Problem: `RAG system not initialized`

**Symptoms:**
```
RAG system not initialized
Error: NoneType has no attribute...
```

**Solutions:**

1. **Call initialize endpoint first:**
   ```bash
   curl -X POST http://localhost:5000/api/initialize
   ```

2. **Wait for initialization:**
   - First time takes 30-60 seconds
   - Don't send chat requests yet
   - Check terminal for progress

3. **Verify data files exist:**
   ```bash
   # Check data folder
   ls -la backend/data/luatbhyt/
   
   # Should have law.txt
   ls backend/data/luatbhyt/law.txt
   ```

4. **Check Pinecone connection:**
   - Verify API key is correct
   - Check internet connection
   - Test Pinecone API manually

**Prevention:**
- Initialize backend first
- Wait for "RAG initialized successfully" message
- Check logs for detailed errors

---

### Problem: `Ollama connection failed`

**Symptoms:**
```
Error: Connection refused to http://localhost:11434
requests.exceptions.ConnectionError
```

**Solutions:**

1. **Check Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Start Ollama:**
   ```bash
   # On Windows/Mac
   ollama serve
   
   # Or use Ollama app
   # Download from https://ollama.ai
   ```

3. **Verify model is installed:**
   ```bash
   ollama list
   
   # Should show llama3.1 or llama2
   ```

4. **Pull model if missing:**
   ```bash
   ollama pull llama3.1
   # or
   ollama pull llama2
   ```

**Prevention:**
- Start Ollama before backend
- Ensure model is installed
- Keep Ollama process running

---

## Performance Issues

### Problem: `Slow response times`

**Symptoms:**
```
Takes 30+ seconds to respond
"Loading..." spinner visible too long
```

**Solutions:**

1. **Check RAG initialization:**
   - First initialization takes time
   - Subsequent requests should be faster
   - Check logs for timing information

2. **Optimize vector search:**
   ```python
   # In processing.py, reduce top_k
   matches = self.retrieve_relevant_docs(query, top_k=3)
   ```

3. **Check backend logs:**
   ```bash
   # Look for timing information
   # [DEBUG] Gửi request tới Ollama...
   # [DEBUG] Nhận phản hồi từ model!
   ```

4. **Monitor system resources:**
   - Check CPU usage
   - Check memory usage
   - Reduce concurrent requests

**Prevention:**
- Profile code to find bottlenecks
- Optimize chunk size and overlap
- Use faster embedding models

---

### Problem: `High memory usage`

**Symptoms:**
```
Application uses 1GB+ memory
System becomes slow after running
```

**Solutions:**

1. **Check what's consuming memory:**
   ```bash
   # Linux/Mac
   ps aux | grep python
   
   # Windows: Task Manager
   ```

2. **Reduce model size:**
   ```python
   # Use smaller model
   self.vector_model = SentenceTransformer("all-MiniLM-L6-v2")
   # Instead of larger models
   ```

3. **Limit document storage:**
   - Only load necessary documents
   - Archive old documents
   - Use smaller chunks

4. **Restart backend periodically:**
   - Kills memory leaks
   - Clears accumulated data
   - Fresh initialization

**Prevention:**
- Monitor memory usage regularly
- Use profiling tools
- Implement cleanup routines

---

## Browser-Specific Issues

### Chrome/Edge

**Issue: Service Worker errors**
```javascript
// Disable service workers if causing issues
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(registrations => {
        registrations.forEach(r => r.unregister());
    });
}
```

**Solution:** Clear site data in Chrome settings

---

### Firefox

**Issue: Mixed content (HTTP/HTTPS)**
```
Mixed Content: The page was loaded over HTTPS, 
but requested an insecure resource
```

**Solution:**
- Use HTTPS for both frontend and backend
- Or use HTTP for both in development

---

### Safari

**Issue: localStorage disabled in private mode**
```
QuotaExceededError: DOM Exception 22
```

**Solution:**
- Test in normal mode
- Add try-catch around localStorage calls

---

## Advanced Debugging

### Enable Debug Logging

**Backend:**
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Detailed information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

**Frontend:**
```javascript
// In main.js
const DEBUG = true;

function log(...args) {
    if (DEBUG) console.log('[DEBUG]', ...args);
}

log('App initialized');
```

---

### Network Debugging

**Using Developer Tools:**
1. Open F12 → Network tab
2. Send a chat message
3. Click on POST /api/chat request
4. View:
   - Request headers
   - Request body
   - Response headers
   - Response body
   - Timing

**Timing Breakdown:**
```
Queueing: Time waiting in queue
DNS: Domain name resolution
Connection: TCP connection time
TLS: SSL/TLS handshake (HTTPS)
Request: Time to send request
Waiting (TTFB): Backend processing time
Content Download: Response transfer time
```

---

### Using curl for API Testing

```bash
# Health check
curl http://localhost:5000/api/health -v

# Initialize
curl -X POST http://localhost:5000/api/initialize \
  -H "Content-Type: application/json" \
  -v

# Chat with full details
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Test?"}' \
  -w "\n%{time_total}s total\n" \
  -v
```

---

## FAQ

### Q: How do I change the Ollama model?

**A:** Edit `processing.py`:
```python
# Change model in generate_response
response = requests.post(
    url="http://localhost:11434/api/generate",
    json={
        "model": "llama2",  # Change this
        # ...
    }
)
```

---

### Q: Can I use a different vector database?

**A:** Yes! Modify `processing.py` to use:
- Weaviate
- Qdrant
- Chroma
- Milvus
- Elasticsearch

Just replace Pinecone client with your database.

---

### Q: How do I add more law documents?

**A:** Add `.txt` files to `backend/data/luatbhyt/` folder. They'll be automatically loaded when RAG initializes.

---

### Q: Can I deploy this on AWS/GCP?

**A:** Yes! See CONFIGURATION.md for deployment options:
- Docker containers
- Kubernetes
- Cloud run services
- EC2 instances

---

### Q: How do I add authentication?

**A:** Add Flask-Login:
```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    # Protected endpoint
```

---

### Q: How do I export chat history?

**A:** Add endpoint:
```python
@app.route('/api/export', methods=['GET'])
def export_history():
    # Get from localStorage on frontend
    # Or save to database on backend
    pass
```

---

### Q: Why is initialization slow?

**A:** It needs to:
1. Load SentenceTransformer model (~100MB)
2. Read all documents
3. Create embeddings for each chunk
4. Upload to Pinecone

First time: 30-60 seconds
Subsequent: Instant

---

### Q: Can I use this offline?

**A:** Partially:
- Frontend: Fully offline (after loaded)
- Backend: Needs Ollama (local), Pinecone (cloud)
- For full offline: Use local vector DB + Ollama

---

## Getting Help

1. **Check Logs:**
   - Frontend: Browser Console (F12)
   - Backend: Terminal output

2. **Read Documentation:**
   - README.md - Overview
   - QUICK_START.md - Setup
   - API_DOCUMENTATION.md - API details
   - PROJECT_STRUCTURE.md - Architecture

3. **Common Solutions:**
   - Hard refresh page (Ctrl+Shift+R)
   - Restart backend (Ctrl+C then python app.py)
   - Clear cache/localStorage (DevTools)
   - Check .env file for typos

4. **Debug Checklist:**
   - ✅ Backend running? (curl health endpoint)
   - ✅ Frontend loaded? (check console)
   - ✅ CORS working? (check Network tab)
   - ✅ API key valid? (check .env)
   - ✅ Data files exist? (check data folder)
   - ✅ Ollama running? (if using local LLM)

---

**Still stuck?** Review the debug sections above or reach out for support!

---

Last Updated: January 2024
