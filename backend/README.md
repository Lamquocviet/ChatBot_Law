# Configuration Guide

## Environment Variables (.env)

### Required Variables

#### Pinecone Configuration
```env
PINECONE_API_KEY=pcsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Get from: https://www.pinecone.io/
- Purpose: Vector database for document retrieval
- Required: Yes

### Flask Configuration

#### Host and Port
```env
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```
- `FLASK_HOST`: Server binding address
  - `0.0.0.0`: Listen on all interfaces (production)
  - `127.0.0.1`: Local only (development)
- `FLASK_PORT`: Server port (default: 5000)

#### Debug Mode
```env
FLASK_DEBUG=False
```
- `True`: Enable auto-reload and detailed errors (development only)
- `False`: Production mode
- ⚠️ Never set to True in production!

### Frontend Configuration

#### API URL
```env
FRONTEND_API_URL=http://localhost:5000
```
- Base URL for all API calls from frontend
- Must match Flask server address
- Development: `http://localhost:5000`
- Production: `https://yourdomain.com/api`

### Optional Advanced Configuration

```env
# RAG Configuration
RAG_DATA_FOLDER=data/luatbhyt
RAG_MODEL_NAME=all-MiniLM-L6-v2
RAG_CHUNK_SIZE=1500
RAG_CHUNK_OVERLAP=200
RAG_TOP_K=5
RAG_SIMILARITY_THRESHOLD=0.35

# Ollama Configuration (if using local LLM)
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1

# CORS Configuration
CORS_ORIGINS=*
CORS_METHODS=GET,POST,OPTIONS

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Database
VECTORDB_DIMENSION=384
VECTORDB_METRIC=cosine
```

---

## Configuration Files

### Frontend Configuration (index.html)

Modify these values in the HTML:

```html
<!-- API Base URL (in main.js) -->
<script>
const API_BASE_URL = 'http://localhost:5000/api';
const CHAT_STORAGE_KEY = 'chat_history';
const DARK_MODE_STORAGE_KEY = 'dark_mode_enabled';
</script>
```

### Backend Configuration (processing.py)

```python
class RAG:
    def __init__(self, data_folder="data/luatbhyt"):
        # Chunk configuration
        chunk_size = 1500
        chunk_overlap = 200
        
        # Vector database
        vector_dimension = 384
        vector_metric = "cosine"
        
        # Retrieval
        top_k = 5
        threshold = 0.35
```

---

## Environment Setup by Use Case

### Development Environment

```env
PINECONE_API_KEY=your_dev_api_key

FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True

FRONTEND_API_URL=http://localhost:5000

OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

LOG_LEVEL=DEBUG
```

### Production Environment

```env
PINECONE_API_KEY=your_prod_api_key

FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=False

FRONTEND_API_URL=https://yourdomain.com

CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

LOG_LEVEL=INFO
LOG_FILE=/var/log/rag-chatbot/app.log
```

### Testing Environment

```env
PINECONE_API_KEY=test_api_key

FLASK_HOST=127.0.0.1
FLASK_PORT=5001
FLASK_DEBUG=True

FRONTEND_API_URL=http://localhost:5001

RAG_DATA_FOLDER=tests/data
```

---

## Configuration Validation

### Check Configuration
```python
# In Python shell
import os
from dotenv import load_dotenv

load_dotenv()

print("PINECONE_API_KEY:", os.getenv('PINECONE_API_KEY')[:10] + "***")
print("FLASK_HOST:", os.getenv('FLASK_HOST'))
print("FLASK_PORT:", os.getenv('FLASK_PORT'))
print("FRONTEND_API_URL:", os.getenv('FRONTEND_API_URL'))
```

### Check Frontend Configuration
```javascript
// In browser console (F12)
console.log("API_BASE_URL:", API_BASE_URL);
fetch(API_BASE_URL + '/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

---

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  rag-backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      PINECONE_API_KEY: ${PINECONE_API_KEY}
      FLASK_HOST: 0.0.0.0
      FLASK_PORT: 5000
      FLASK_DEBUG: False
    volumes:
      - ./backend/data:/app/data
    restart: unless-stopped

  rag-frontend:
    image: nginx:alpine
    ports:
      - "8000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - rag-backend
    restart: unless-stopped
```

### Run with Docker

```bash
docker-compose up
```

---

## NGINX Reverse Proxy Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/rag-chatbot/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # HTTPS redirect
    if ($scheme != "https") {
        return 301 https://$server_name$request_uri;
    }
}
```

---

## SSL/HTTPS Configuration

### Using Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Update Configuration

```env
FRONTEND_API_URL=https://yourdomain.com
CORS_ORIGINS=https://yourdomain.com
```

---

## Systemd Service Configuration

Create `/etc/systemd/system/rag-chatbot.service`:

```ini
[Unit]
Description=RAG Chatbot Flask Application
After=network.target

[Service]
Type=notify
User=rag-chatbot
WorkingDirectory=/opt/rag-chatbot/backend
Environment="PATH=/opt/rag-chatbot/backend/venv/bin"
EnvironmentFile=/opt/rag-chatbot/backend/.env
ExecStart=/opt/rag-chatbot/backend/venv/bin/gunicorn \
    --workers 4 \
    --bind 0.0.0.0:5000 \
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

### Manage Service

```bash
# Start
sudo systemctl start rag-chatbot

# Stop
sudo systemctl stop rag-chatbot

# Restart
sudo systemctl restart rag-chatbot

# Check status
sudo systemctl status rag-chatbot

# Enable on boot
sudo systemctl enable rag-chatbot

# View logs
sudo journalctl -u rag-chatbot -f
```

---

## Performance Tuning

### Backend Optimization

```python
# In app.py
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/chat')
@cache.cached(timeout=300, query_string=True)
def chat():
    # Cached response
    pass
```

### Frontend Optimization

```javascript
// In main.js
const CACHE_EXPIRY = 5 * 60 * 1000; // 5 minutes
const requestCache = new Map();

async function cachedFetch(url, options) {
    const key = url + JSON.stringify(options);
    if (requestCache.has(key)) {
        return requestCache.get(key);
    }
    const result = await fetch(url, options);
    requestCache.set(key, result);
    setTimeout(() => requestCache.delete(key), CACHE_EXPIRY);
    return result;
}
```

### Database Optimization

```env
# Increase connection pool
PINECONE_MAX_CONNECTIONS=10
PINECONE_CONNECTION_TIMEOUT=30

# Increase batch size
RAG_BATCH_SIZE=100
```

---

## Monitoring and Logging

### Enable Logging

```env
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_FORMAT=json
```

### View Logs

```bash
# Real-time
tail -f logs/app.log

# With filtering
tail -f logs/app.log | grep ERROR

# Using journalctl
journalctl -u rag-chatbot -n 100
```

### Setup Log Rotation

Create `/etc/logrotate.d/rag-chatbot`:

```
/var/log/rag-chatbot/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 rag-chatbot rag-chatbot
    sharedscripts
    postrotate
        systemctl reload rag-chatbot > /dev/null 2>&1 || true
    endscript
}
```

---

## Security Configuration

### API Security

```python
# In app.py
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("100 per hour")
def chat():
    # Rate limited endpoint
    pass
```

### CORS Security

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://yourdomain.com",
            "https://www.yourdomain.com"
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### .env Security

```bash
# Never commit .env
echo ".env" >> .gitignore

# Use restricted permissions
chmod 600 .env

# Use environment variables in production
export PINECONE_API_KEY="your_key"
```

---

## Troubleshooting Configuration

### "Module not found" Error

```bash
# Verify virtual environment
which python
# Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "Port already in use" Error

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### "CORS Error"

Check configuration:
1. FLASK_DEBUG=False disables permissive CORS
2. Update FRONTEND_API_URL in frontend
3. Add domain to CORS_ORIGINS in .env

---

## Configuration Best Practices

1. ✅ Use `.env` files (don't hardcode secrets)
2. ✅ Different configs for dev/prod/test
3. ✅ Version control `.env.example` (without keys)
4. ✅ Use strong API keys
5. ✅ Rotate keys periodically
6. ✅ Use environment variables in production
7. ✅ Log configuration on startup (without secrets)
8. ✅ Validate configuration on startup
9. ✅ Use HTTPS in production
10. ✅ Enable rate limiting

---

Last Updated: 2024-01-01
