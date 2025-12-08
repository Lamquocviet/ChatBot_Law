# Project Structure Guide

## Complete Project Tree

```
RAG/
│
├── 📄 README.md                           ← Start here! Complete overview
├── 📄 QUICK_START.md                      ← 5-minute setup guide  
├── 📄 API_DOCUMENTATION.md                ← All API endpoints explained
├── 📄 CONFIGURATION.md                    ← Configuration and deployment
├── 📄 INTEGRATION_SUMMARY.md              ← What was built (this project)
│
├── backend/                               ← Python Flask Backend
│   ├── 🆕 app.py                         ← Flask API Server (MAIN)
│   ├── 📝 main.py                        ← Original console interface
│   ├── processing.py                     ← RAG logic & LLM integration
│   ├── jsonData.js                       ← Law data reference
│   ├── requirements.txt                  ← Python dependencies
│   ├── 📝 .env                           ← Environment configuration
│   ├── .gitignore
│   ├── __pycache__/                      ← Python cache
│   ├── data/                             ← Knowledge base
│   │   └── luatbhyt/                     ← Law documents
│   │       ├── law.txt                   ← Main law document
│   │       └── *.txt                     ← Additional documents
│   ├── demuc/                            ← HTML documents
│   │   ├── *.html                        ← Document files
│   │   └── ...
│   └── searching/                        ← Search functionality
│       └── crawler/                      ← Web crawler
│
├── frontend/                              ← Web Interface
│   ├── 🆕 main.js                       ← Chat Client (COMPLETELY REWRITTEN)
│   │   ├── API Communication
│   │   ├── Chat Management
│   │   ├── History Management
│   │   ├── Message Formatting
│   │   └── UI State Management
│   ├── index.html                        ← HTML Structure
│   │   ├── Sidebar (Chat History)
│   │   ├── Chat Area (Messages)
│   │   ├── Input Area (Question Input)
│   │   └── Welcome Screen
│   ├── 📝 style.css                      ← Styling (UPDATED)
│   │   ├── Layout & Grid
│   │   ├── Chat Messages
│   │   ├── Dark Mode
│   │   ├── Animations
│   │   ├── Responsive Design
│   │   └── Loading Indicators
│   └── jsonData.js                       ← Law category data
│
└── .gitignore                             ← Git ignore rules

Legend:
  🆕 = New file created
  📝 = Modified file
  📄 = Documentation
  = Existing file
```

---

## File Dependencies & Relationships

```
┌─────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  index.html                                             │
│  ├─ Links: style.css, main.js, jsonData.js            │
│  └─ Events: onclick handlers call main.js functions   │
│                                                         │
│  main.js (COMPLETELY REWRITTEN)                        │
│  ├─ API Client Functions                              │
│  ├─ Chat Logic                                         │
│  ├─ Message Formatting                                │
│  ├─ History Management                                │
│  └─ Event Listeners                                    │
│                                                         │
│  style.css (UPDATED)                                   │
│  ├─ Layout Styles                                     │
│  ├─ Dark Mode                                          │
│  ├─ Animations                                         │
│  └─ Loading Indicators                                 │
│                                                         │
│  jsonData.js                                            │
│  └─ Law categories & topics (reference data)          │
│                                                         │
└─────────────────────────────────────────────────────────┘
        │
        │ HTTP Requests/Responses (JSON)
        │
┌───────▼───────────────────────────────────────────────┐
│            FLASK API SERVER (app.py)                  │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Routes:                                             │
│  ├─ POST   /api/chat                                │
│  ├─ POST   /api/initialize                          │
│  ├─ GET    /api/health                              │
│  ├─ GET    /api/articles/<id>                       │
│  └─ POST   /api/chat/stream                         │
│                                                      │
│  Initialization:                                     │
│  ├─ Load .env (Python-dotenv)                       │
│  ├─ Create CORS app                                 │
│  └─ Initialize RAG instance                         │
│                                                      │
└──────────┬──────────────────────────────────────────┘
           │
           │ Uses
           │
┌──────────▼──────────────────────────────────────────┐
│         PROCESSING.PY (RAG System)                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  RAG Class:                                         │
│  ├─ __init__()                                      │
│  │  └─ Load SentenceTransformer model              │
│  │  └─ Connect to Pinecone                         │
│  │  └─ Create/load vector index                    │
│  │                                                 │
│  ├─ create_vectordb()                              │
│  │  ├─ Read documents from data/luatbhyt/          │
│  │  ├─ Split into chunks                           │
│  │  ├─ Generate embeddings                         │
│  │  └─ Upload to Pinecone                          │
│  │                                                 │
│  ├─ retrieve_relevant_docs()                       │
│  │  ├─ Embed query                                 │
│  │  ├─ Search Pinecone                             │
│  │  └─ Filter by threshold                         │
│  │                                                 │
│  ├─ generate_response()                            │
│  │  ├─ Search raw article                          │
│  │  ├─ If found: return article                    │
│  │  ├─ Else: RAG pipeline                          │
│  │  │   ├─ Retrieve context                        │
│  │  │   ├─ Build prompt                            │
│  │  │   └─ Call LLM (Ollama)                       │
│  │  └─ Return response                             │
│  │                                                 │
│  └─ search_raw_article()                           │
│     └─ Extract article by number                   │
│                                                     │
└──────────┬──────────────────────────────────────────┘
           │
           │ Uses
           │
    ┌──────┴──────┐
    │             │
┌───▼───────┐  ┌──▼────────────┐
│ Pinecone  │  │ Ollama LLM    │
│ Vector DB │  │ (Local)       │
│           │  │               │
│ Embeddings│  │ llamal3.1     │
│ Search    │  │ or llama2     │
│ Storage   │  │               │
└───────────┘  └───────────────┘
```

---

## Data Flow Diagrams

### 1. Chat Request Flow

```
┌─────────────────────┐
│  User Enters Text   │
│  & Presses Enter    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────────────┐
│  JavaScript Event Handler   │
│  askQuestion()              │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Validate Input             │
│  - Check if not empty       │
│  - Trim whitespace          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Show Loading Indicator     │
│  Disable Send Button        │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  POST /api/chat             │
│  {question: "..."}          │
└────────┬────────────────────┘
         │ HTTP
         ▼
┌─────────────────────────────┐
│  Flask Backend              │
│  def chat():                │
│  ├─ Parse JSON              │
│  ├─ Validate question       │
│  ├─ Initialize RAG          │
│  └─ Generate response       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  RAG Pipeline               │
│  ├─ Search article          │
│  ├─ Retrieve docs           │
│  ├─ Create context          │
│  └─ Call LLM                │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Return Response            │
│  {status, question, answer} │
└────────┬────────────────────┘
         │ JSON Response
         ▼
┌─────────────────────────────┐
│  JavaScript                 │
│  ├─ Parse response          │
│  ├─ Check status            │
│  └─ Add to chat display     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Format Message             │
│  ├─ Parse markdown          │
│  ├─ Highlight articles      │
│  └─ Add animations          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Update UI                  │
│  ├─ Add message to chat     │
│  ├─ Scroll to bottom        │
│  ├─ Hide loading            │
│  └─ Enable send button      │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Save to History            │
│  └─ localStorage            │
└─────────────────────────────┘
```

### 2. Initialization Flow

```
┌──────────────────────┐
│  App Loads          │
│  (DOMContentLoaded)  │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────────┐
│  Apply Dark Mode        │
│  (if saved)             │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│  Load Chat History      │
│  from localStorage      │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│  Initialize Backend     │
│  POST /api/initialize   │
└─────────┬────────────────┘
          │ HTTP
          ▼
┌──────────────────────────┐
│  Backend (app.py)       │
│  ├─ Create RAG instance │
│  ├─ Load model          │
│  ├─ Connect Pinecone    │
│  └─ Create/load index   │
└─────────┬────────────────┘
          │
          ▼
┌──────────────────────────┐
│  Load Documents         │
│  from data/luatbhyt/    │
├──────────────────────────┤
│  ├─ Read law.txt        │
│  ├─ Split chunks        │
│  ├─ Generate embeddings │
│  └─ Upload to Pinecone  │
└─────────┬────────────────┘
          │ (30-60 seconds)
          ▼
┌──────────────────────────┐
│  Return Success         │
│  {status: success}      │
└─────────┬────────────────┘
          │ JSON Response
          ▼
┌──────────────────────────┐
│  Show Success Message   │
│  "✓ 系统已就绪"         │
├──────────────────────────┤
│  App Ready for Chat     │
└──────────────────────────┘
```

---

## Component Interaction Map

```
                    ┌──────────────┐
                    │   BROWSER    │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐        ┌────────┐        ┌─────────┐
    │ HTML   │        │ CSS    │        │   JS    │
    │        │        │        │        │         │
    │Layout  │        │Styles  │        │ Logic   │
    │        │        │        │        │         │
    └───┬────┘        └───┬────┘        └────┬────┘
        │                 │                  │
        │ Renders      │ Renders         │ Executes
        │              │                 │
        ▼              ▼                 ▼
    ┌──────────────────────────────────────────┐
    │          DOM (Document Object Model)     │
    ├──────────────────────────────────────────┤
    │  - Sidebar (Chat History)                │
    │  - Chat Area (Messages)                  │
    │  - Input Area (Input Field)              │
    │  - Welcome Screen                        │
    └──────────┬───────────────────────────────┘
               │
        ┌──────▼──────┐
        │ Event Loop  │
        ├─────────────┤
        │ Click       │
        │ KeyPress    │
        │ Change      │
        └──────┬──────┘
               │
        ┌──────▼──────────────┐
        │ JavaScript Handlers │
        ├─────────────────────┤
        │ askQuestion()       │
        │ newChat()           │
        │ toggleDarkMode()    │
        │ deleteChat()        │
        │ handleKeyPress()    │
        └──────┬──────────────┘
               │
        ┌──────▼──────────────┐
        │  Fetch API Calls    │
        ├─────────────────────┤
        │ POST /api/chat      │
        │ POST /api/initialize│
        │ GET /api/health     │
        └──────┬──────────────┘
               │ HTTP
        ┌──────▼─────────────────────┐
        │   Flask Backend (app.py)   │
        ├────────────────────────────┤
        │  - Request Validation      │
        │  - Error Handling          │
        │  - RAG Integration         │
        │  - Response Formation      │
        └──────┬────────────────────┘
               │
        ┌──────▼────────────────┐
        │  RAG System (processing.py)
        ├───────────────────────┤
        │  - Vector DB Query    │
        │  - LLM Generation     │
        │  - Context Building   │
        └──────┬────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
    ┌────────┐    ┌────────────┐
    │Pinecone│    │  Ollama    │
    │ Vector │    │    LLM     │
    │  DB    │    │            │
    └────────┘    └────────────┘
```

---

## File-by-File Breakdown

### Backend Files

#### `app.py` - Flask API Server
```python
Purpose: Main API server providing REST endpoints
Size: ~300 lines
Key Functions:
  - initialize_rag(): Initialize RAG system
  - health_check(): Check server status
  - chat(): Main chat endpoint
  - get_article(): Get specific article
  - Error handlers: 404, 500
```

#### `processing.py` - RAG Logic (Existing)
```python
Purpose: RAG pipeline and LLM integration
Classes:
  - RAG: Main RAG class with methods:
    - create_vectordb()
    - retrieve_relevant_docs()
    - generate_response()
    - search_raw_article()
    - read_text()
    - text_to_docs()
    - docs_to_index()
```

#### `.env` - Configuration
```env
Purpose: Store sensitive configuration
Contains:
  - PINECONE_API_KEY
  - FLASK_HOST, FLASK_PORT
  - FLASK_DEBUG flag
  - FRONTEND_API_URL
```

### Frontend Files

#### `main.js` - Chat Client & Logic
```javascript
Purpose: All client-side functionality
Size: ~600 lines
Key Functions:
  - initializeBackend(): Initialize RAG
  - askQuestion(): Send chat message
  - addMessageToChat(): Display message
  - formatMessageContent(): Format markdown
  - saveChatHistory(): Persist history
  - loadChatHistory(): Restore history
  - newChat(): Start new session
  - toggleDarkMode(): Switch theme
Variables:
  - API_BASE_URL: Backend URL
  - currentChatId: Active chat
  - chatSessions: All chat data
  - isLoading: Request state
```

#### `index.html` - UI Layout
```html
Purpose: HTML structure
Sections:
  - Sidebar: Chat history
  - Chat Area: Messages display
  - Input Area: Question input
  - Welcome Screen: Initial view
External Resources:
  - style.css: Styling
  - main.js: Logic
  - Highlight.js: Code syntax
  - Marked: Markdown parsing
```

#### `style.css` - Styling & Animations
```css
Purpose: Visual presentation
Features:
  - CSS Grid/Flexbox layout
  - Dark mode variables
  - Responsive breakpoints
  - Animation keyframes
  - Loading indicators
  - Message formatting
Sections:
  - Variables (:root)
  - Layout
  - Sidebar
  - Chat Area
  - Messages
  - Input
  - Dark Mode
  - Animations
```

---

## Development Workflow

### 1. Adding a New Feature

```
1. Plan the feature
   │
   ▼
2. Backend (if needed)
   ├─ Add endpoint in app.py
   ├─ Test with curl
   └─ Commit changes
   │
   ▼
3. Frontend
   ├─ Add JavaScript function in main.js
   ├─ Add HTML elements in index.html (if needed)
   ├─ Add CSS in style.css (if needed)
   ├─ Test in browser
   └─ Commit changes
   │
   ▼
4. Integration Testing
   ├─ Test full flow
   ├─ Check responsiveness
   └─ Verify dark mode
   │
   ▼
5. Documentation
   ├─ Update README
   ├─ Update API_DOCUMENTATION
   └─ Add code comments
```

### 2. Bug Fixing

```
1. Identify Issue
   ├─ Frontend: DevTools console
   └─ Backend: Terminal logs
   │
   ▼
2. Locate Code
   ├─ Search file content
   └─ Review related functions
   │
   ▼
3. Fix Bug
   ├─ Make minimal changes
   └─ Test thoroughly
   │
   ▼
4. Verify Fix
   ├─ Reproduce original issue
   └─ Confirm fix works
   │
   ▼
5. Commit
   └─ Clear commit message
```

---

## Testing Checkpoints

```
┌─────────────────────────────────────────────┐
│ Unit Testing                                │
├─────────────────────────────────────────────┤
│ ├─ Backend: Test each endpoint             │
│ │  ├─ /health                              │
│ │  ├─ /initialize                          │
│ │  ├─ /chat                                │
│ │  └─ /articles/{id}                       │
│ │                                           │
│ └─ Frontend: Test each function            │
│    ├─ askQuestion()                        │
│    ├─ addMessageToChat()                   │
│    ├─ saveChatHistory()                    │
│    └─ toggleDarkMode()                     │
│                                             │
│ Integration Testing                        │
├─────────────────────────────────────────────┤
│ ├─ Backend to Pinecone connection          │
│ ├─ Backend to Ollama connection            │
│ ├─ Frontend to Backend API                 │
│ ├─ Frontend to localStorage                │
│ └─ Full chat flow end-to-end               │
│                                             │
│ UI Testing                                  │
├─────────────────────────────────────────────┤
│ ├─ Message display                         │
│ ├─ Chat history display                    │
│ ├─ Dark mode toggle                        │
│ ├─ Loading indicators                      │
│ ├─ Error messages                          │
│ └─ Responsive design                       │
│                                             │
│ Performance Testing                        │
├─────────────────────────────────────────────┤
│ ├─ Page load time                          │
│ ├─ API response time                       │
│ ├─ Message rendering time                  │
│ └─ Memory usage                            │
└─────────────────────────────────────────────┘
```

---

## Deployment Checklist

```
Backend Setup
├─ [ ] .env created with API keys
├─ [ ] Virtual environment setup
├─ [ ] Dependencies installed
├─ [ ] app.py runs without errors
└─ [ ] Health endpoint responds

Frontend Setup
├─ [ ] index.html loads
├─ [ ] main.js executes
├─ [ ] style.css applies
├─ [ ] No console errors
└─ [ ] Can send chat messages

Integration
├─ [ ] Frontend connects to backend
├─ [ ] Chat messages are sent/received
├─ [ ] History is saved
├─ [ ] Dark mode works
└─ [ ] All features function

Production
├─ [ ] HTTPS enabled (if needed)
├─ [ ] CORS configured
├─ [ ] Rate limiting enabled
├─ [ ] Logging configured
├─ [ ] Monitoring setup
└─ [ ] Backup system ready
```

---

This guide provides a complete understanding of the project structure and how all components work together.

For more details, refer to:
- README.md - Project overview
- API_DOCUMENTATION.md - API details
- QUICK_START.md - Setup guide
- CONFIGURATION.md - Configuration options

---

Last Updated: January 2024
