# API Documentation - RAG Chatbot

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently no authentication required. (Add JWT tokens for production)

## Content-Type
All requests and responses use `application/json`

---

## Endpoints

### 1. Health Check

**Purpose:** Verify server and RAG system status

```http
GET /health
```

**Parameters:** None

**Response (200 OK):**
```json
{
  "status": "ok",
  "rag_initialized": true,
  "error": null
}
```

**Response (503 Service Unavailable):**
```json
{
  "status": "error",
  "rag_initialized": false,
  "error": "RAG initialization failed: [error details]"
}
```

**Example:**
```bash
curl http://localhost:5000/api/health
```

---

### 2. Initialize RAG System

**Purpose:** Initialize vector database and load law documents

```http
POST /initialize
```

**Request Body:**
```json
{}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "RAG system initialized successfully"
}
```

**Response (500 Internal Server Error):**
```json
{
  "status": "error",
  "message": "Failed to initialize RAG system",
  "error": "Connection to Pinecone failed"
}
```

**Notes:**
- First call may take 30-60 seconds
- Subsequent calls return immediately if already initialized
- Required before sending chat requests

**Example:**
```bash
curl -X POST http://localhost:5000/api/initialize \
  -H "Content-Type: application/json"
```

---

### 3. Chat (Main Endpoint)

**Purpose:** Send user question and get AI response

```http
POST /chat
```

**Request Body:**
```json
{
  "question": "What is health insurance law in Vietnam?"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "question": "What is health insurance law in Vietnam?",
  "answer": "Health insurance law in Vietnam is...",
  "timestamp": "2024-01-01T12:00:00"
}
```

**Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Missing 'question' field in request"
}
```

**Response (500 Internal Server Error):**
```json
{
  "status": "error",
  "message": "Error processing request",
  "error": "LLM connection failed"
}
```

**Request Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| question | string | Yes | User's question |

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| status | string | "success" or "error" |
| question | string | Echo of user's question |
| answer | string | AI's response |
| timestamp | string | ISO 8601 timestamp |

**Notes:**
- Minimum question length: 1 character
- RAG system must be initialized first
- Response time: 5-15 seconds depending on question
- Supports Vietnamese, English languages

**Example:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Luật Bảo hiểm y tế là gì?"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "Luật Bảo hiểm y tế là gì?",
  "answer": "Luật Bảo hiểm y tế là luật quy định về...",
  "timestamp": "2024-01-01T12:00:00"
}
```

---

### 4. Chat Streaming (Future Enhancement)

**Purpose:** Get streamed response for real-time display

```http
POST /chat/stream
```

**Request Body:**
```json
{
  "question": "Điều 1 nói về cái gì?"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "question": "Điều 1 nói về cái gì?",
  "answer": "Luật này quy định..."
}
```

**Note:** Currently returns complete response. Future version will support streaming.

---

### 5. Get Specific Article

**Purpose:** Retrieve specific article from law documents

```http
GET /articles/{article_number}
```

**URL Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| article_number | integer | Article number (1-onwards) |

**Response (200 OK):**
```json
{
  "status": "success",
  "article": 1,
  "content": "Điều 1: Phạm vi điều chỉnh..."
}
```

**Response (404 Not Found):**
```json
{
  "status": "error",
  "message": "Article 999 not found"
}
```

**Example:**
```bash
curl http://localhost:5000/api/articles/1
curl http://localhost:5000/api/articles/5
```

---

## Error Codes

### HTTP Status Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing/invalid parameters |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal server error |
| 503 | Service Unavailable | RAG not initialized |

### API Error Response Format

```json
{
  "status": "error",
  "message": "Human-readable error message",
  "error": "Detailed technical error (optional)"
}
```

---

## Request/Response Examples

### Example 1: Simple Question

**Request:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Mức đóng BHYT hiện nay là bao nhiêu?"
  }'
```

**Response:**
```json
{
  "status": "success",
  "question": "Mức đóng BHYT hiện nay là bao nhiêu?",
  "answer": "Theo Luật Bảo hiểm y tế...",
  "timestamp": "2024-01-01T12:30:45"
}
```

### Example 2: Article Lookup

**Request:**
```bash
curl http://localhost:5000/api/articles/2
```

**Response:**
```json
{
  "status": "success",
  "article": 2,
  "content": "Điều 2: Đối tượng tham gia bảo hiểm y tế bao gồm..."
}
```

### Example 3: Error Handling

**Request (Missing question):**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "status": "error",
  "message": "Missing \"question\" field in request"
}
```

---

## Rate Limiting

Currently no rate limiting implemented.

**Recommended for Production:**
- 100 requests per minute per IP
- 10 concurrent requests per session
- Response timeout: 30 seconds

---

## CORS (Cross-Origin Resource Sharing)

**Allowed Origins:** All (`*`)

**Allowed Methods:** GET, POST, OPTIONS

**Allowed Headers:** Content-Type, Authorization

**Example CORS Request:**
```javascript
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: 'Your question here'
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

---

## Best Practices

### 1. Always Initialize First
```javascript
// Initialize RAG system
await fetch('/api/initialize', { method: 'POST' });

// Then send chat request
await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ question: '...' })
});
```

### 2. Error Handling
```javascript
try {
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ question })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const data = await response.json();
  
  if (data.status === 'error') {
    console.error('API Error:', data.message);
  } else {
    console.log('Response:', data.answer);
  }
} catch (error) {
  console.error('Network Error:', error);
}
```

### 3. Add Timeout
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000);

fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ question }),
  signal: controller.signal
})
.finally(() => clearTimeout(timeoutId));
```

### 4. Retry Logic
```javascript
async function chatWithRetry(question, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify({ question })
      });
      return await response.json();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

---

## Webhook/Callback (Future)

Reserved for future implementation of:
- Chat completion callbacks
- Typing indicators
- Real-time notifications

---

## API Versioning

Current Version: **v1**

Future versions planned:
- v2: Streaming responses
- v3: Multi-language support
- v4: User authentication

---

## Testing

### Using curl

```bash
# Health check
curl http://localhost:5000/api/health

# Initialize
curl -X POST http://localhost:5000/api/initialize

# Chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"Hỏi gì?"}'
```

### Using JavaScript/Fetch

```javascript
// Health check
fetch('http://localhost:5000/api/health').then(r => r.json());

// Chat
fetch('http://localhost:5000/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: 'Your question'})
}).then(r => r.json());
```

### Using Python/Requests

```python
import requests

# Health check
r = requests.get('http://localhost:5000/api/health')
print(r.json())

# Chat
r = requests.post('http://localhost:5000/api/chat', 
  json={'question': 'Your question'})
print(r.json())
```

---

## Troubleshooting API Calls

### Connection Refused
- Backend not running
- Check port 5000 is free
- Verify FLASK_HOST and FLASK_PORT in .env

### Timeout
- RAG system still initializing
- Backend overloaded
- Increase timeout value

### Empty Response
- Question too short
- Data files missing
- RAG not initialized

---

## Support

For issues or questions about the API, refer to:
- GitHub Issues
- Documentation: README.md
- Quick Start: QUICK_START.md

---

Last Updated: 2024-01-01
