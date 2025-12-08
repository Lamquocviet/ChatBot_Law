/**
 * Frontend API Client and Chat Logic
 * Handles communication between UI and backend API
 */

// Configuration
// Use 127.0.0.1 to avoid IPv6/localhost resolution issues in some environments
const API_BASE_URL = "http://127.0.0.1:5000/api";
// Expose for debugging in browser console
window.API_BASE_URL = API_BASE_URL;
const CHAT_STORAGE_KEY = "chat_history";
const DARK_MODE_STORAGE_KEY = "dark_mode_enabled";

// State management
let currentChatId = null;
let chatSessions = new Map();
let isLoading = false;
let isDarkMode = localStorage.getItem(DARK_MODE_STORAGE_KEY) === "true";

/**
 * Initialize the application
 */
document.addEventListener("DOMContentLoaded", () => {
  console.log("Initializing chatbot application...");

  // Apply dark mode if saved
  if (isDarkMode) {
    document.body.classList.add("dark-mode");
  }

  // Initialize chat
  newChat();

  // Load chat history
  loadChatHistory();

  // Initialize backend
  initializeBackend();
});

/**
 * Initialize backend RAG system
 */
async function initializeBackend() {
  try {
    const response = await fetch(`${API_BASE_URL}/initialize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();

    if (data.status === "success") {
      console.log("Backend RAG system initialized successfully");
      showSystemMessage("✓ Hệ thống đã sẵn sàng");
    } else {
      console.error("Backend initialization failed:", data.error);
      showSystemMessage("⚠ Khởi tạo hệ thống thất bại, vui lòng tải lại trang");
    }
  } catch (error) {
    console.error("Error initializing backend:", error);
    showSystemMessage(
      "⚠ Không thể kết nối đến máy chủ, hãy đảm bảo backend đang chạy"
    );
  }
}

/**
 * Send question to backend and get response
 */
async function askQuestion(question = null) {
  // Get question from input if not provided
  if (!question) {
    const questionInput = document.getElementById("question");
    question = questionInput.value.trim();

    if (!question) {
      return;
    }
  }

  // Prevent multiple requests
  if (isLoading) {
    console.log("Request already in progress");
    return;
  }

  isLoading = true;

  try {
    // Clear input
    document.getElementById("question").value = "";

    // Add user message to chat
    addMessageToChat("user", question);

    // Show loading indicator
    showLoadingIndicator();

    // Send request to backend
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
      }),
    });

    const data = await response.json();

    // Remove loading indicator
    hideLoadingIndicator();

    if (data.status === "success") {
      // Add AI response to chat
      addMessageToChat("assistant", data.answer);

      // Save chat history
      saveChatHistory();
    } else {
      // Show error message
      const errorMsg =
        data.error || data.message || "Đã xảy ra lỗi khi xử lý yêu cầu";
      addMessageToChat("error", `❌ Lỗi: ${errorMsg}`);
    }
  } catch (error) {
    console.error("Error sending question:", error);
    hideLoadingIndicator();
    addMessageToChat("error", `❌ Lỗi kết nối: ${error.message}`);
  } finally {
    isLoading = false;
    document.getElementById("question").focus();
  }
}

/**
 * Handle Enter key in input
 */
function handleInputKeyPress(event) {
  if (event.key === "Enter" && !event.shiftKey && !isLoading) {
    event.preventDefault();
    askQuestion();
  }
}

/**
 * Add message to chat display
 */
function addMessageToChat(role, content) {
  const chatArea = document.getElementById("chatArea");

  // Remove welcome container if it exists
  const welcomeContainer = chatArea.querySelector(".welcome-container");
  if (welcomeContainer) {
    welcomeContainer.remove();
  }

  // Create message element
  const messageEl = document.createElement("div");
  messageEl.className = `message message-${role}`;

  // Create content wrapper
  const contentEl = document.createElement("div");
  contentEl.className = "message-content";

  // Format content based on role
  if (role === "user") {
    contentEl.textContent = content;
  } else if (role === "error") {
    contentEl.innerHTML = content;
    contentEl.style.color = "#ff4444";
  } else if (role === "assistant") {
    // Parse markdown and code blocks
    contentEl.innerHTML = formatMessageContent(content);
  } else {
    contentEl.innerHTML = content;
  }

  messageEl.appendChild(contentEl);
  chatArea.appendChild(messageEl);

  // Scroll to bottom
  setTimeout(() => {
    chatArea.scrollTop = chatArea.scrollHeight;
  }, 100);

  // Store message in current session
  if (!chatSessions.has(currentChatId)) {
    chatSessions.set(currentChatId, []);
  }
  chatSessions.get(currentChatId).push({
    role: role,
    content: content,
    timestamp: new Date().toISOString(),
  });
}

/**
 * Format message content with markdown and code highlighting
 */
function formatMessageContent(content) {
  // Escape HTML
  let formatted = escapeHtml(content);

  // Format bold text
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  formatted = formatted.replace(/__(.*?)__/g, "<strong>$1</strong>");

  // Format italic text
  formatted = formatted.replace(/\*(.*?)\*/g, "<em>$1</em>");
  formatted = formatted.replace(/_(.*?)_/g, "<em>$1</em>");

  // Format line breaks
  formatted = formatted.replace(/\n/g, "<br>");

  // Format code blocks
  formatted = formatted.replace(/```(.*?)```/gs, (match, code) => {
    return `<pre><code>${code.trim()}</code></pre>`;
  });

  // Format inline code
  formatted = formatted.replace(/`(.*?)`/g, "<code>$1</code>");

  // Format articles (Điều X)
  formatted = formatted.replace(
    /Điều\s+(\d+)/g,
    '<strong style="color: var(--primary-color)">Điều $1</strong>'
  );

  return formatted;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

/**
 * Show loading indicator
 */
function showLoadingIndicator() {
  const chatArea = document.getElementById("chatArea");

  const loadingEl = document.createElement("div");
  loadingEl.className = "message message-assistant loading-indicator";
  loadingEl.id = "loading-indicator";
  loadingEl.innerHTML = `
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

  chatArea.appendChild(loadingEl);
  chatArea.scrollTop = chatArea.scrollHeight;
}

/**
 * Hide loading indicator
 */
function hideLoadingIndicator() {
  const loadingEl = document.getElementById("loading-indicator");
  if (loadingEl) {
    loadingEl.remove();
  }
}

/**
 * Show system message
 */
function showSystemMessage(message) {
  const chatArea = document.getElementById("chatArea");
  const msgEl = document.createElement("div");
  msgEl.className = "message message-system";
  msgEl.innerHTML = `<div class="message-content">${message}</div>`;
  chatArea.appendChild(msgEl);
}

/**
 * Start a new chat session
 */
function newChat() {
  currentChatId = generateChatId();
  chatSessions.set(currentChatId, []);

  const chatArea = document.getElementById("chatArea");
  chatArea.innerHTML = `
        <div class="welcome-container">
            <div class="welcome-content">
                <h2 class="welcome-title">Xin chào! 👋</h2>
                <p class="welcome-subtitle">Tôi là trợ lý pháp lý chuyên tư vấn về <strong>Luật Bảo hiểm y tế</strong></p>
                
                <div class="welcome-suggestions">
                    <p class="suggestions-title">Bạn có thể hỏi về:</p>
                    <div class="suggestion-grid">
                        <div class="suggestion-card" onclick="askSuggested('Luật Bảo hiểm y tế là gì?')">
                            <span class="icon">📋</span>
                            <span>Luật Bảo hiểm y tế là gì?</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Đối tượng nào bắt buộc tham gia BHYT?')">
                            <span class="icon">👥</span>
                            <span>Đối tượng nào bắt buộc tham gia BHYT?</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Người tham gia BHYT được hưởng những quyền lợi gì?')">
                            <span class="icon">💊</span>
                            <span>Người tham gia BHYT được hưởng những quyền lợi gì?</span>
                        </div>
                        <div class="suggestion-card" onclick="askSuggested('Mức đóng BHYT hiện nay là bao nhiêu?')">
                            <span class="icon">💰</span>
                            <span>Mức đóng BHYT hiện nay là bao nhiêu?</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

  document.getElementById("question").value = "";
  document.getElementById("question").focus();

  updateChatHistoryUI();
  saveChatHistory();
}

/**
 * Ask a suggested question
 */
function askSuggested(question) {
  document.getElementById("question").value = question;
  askQuestion(question);
}

/**
 * Generate unique chat ID
 */
function generateChatId() {
  return "chat_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
}

/**
 * Save chat history to localStorage
 */
function saveChatHistory() {
  const history = {
    sessions: Array.from(chatSessions.entries()).map(([id, messages]) => ({
      id: id,
      messages: messages,
      timestamp: messages[0]?.timestamp || new Date().toISOString(),
    })),
    currentChatId: currentChatId,
  };

  localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(history));
}

/**
 * Load chat history from localStorage
 */
function loadChatHistory() {
  try {
    const stored = localStorage.getItem(CHAT_STORAGE_KEY);

    if (stored) {
      const history = JSON.parse(stored);

      // Restore sessions
      history.sessions.forEach((session) => {
        chatSessions.set(session.id, session.messages);
      });

      // Restore current chat
      if (history.currentChatId && chatSessions.has(history.currentChatId)) {
        currentChatId = history.currentChatId;
        loadChatSession(currentChatId);
      }
    }
  } catch (error) {
    console.error("Error loading chat history:", error);
    currentChatId = generateChatId();
    chatSessions.set(currentChatId, []);
  }

  updateChatHistoryUI();
}

/**
 * Load a specific chat session
 */
function loadChatSession(chatId) {
  if (!chatSessions.has(chatId)) {
    return;
  }

  currentChatId = chatId;
  const chatArea = document.getElementById("chatArea");
  chatArea.innerHTML = "";

  const messages = chatSessions.get(chatId);

  if (messages.length === 0) {
    newChat();
  } else {
    messages.forEach((msg) => {
      addMessageToChat(msg.role, msg.content);
    });
  }

  updateChatHistoryUI();
}

/**
 * Update chat history UI
 */
function updateChatHistoryUI() {
  const historyContainer = document.getElementById("chatHistory");
  historyContainer.innerHTML = "";

  // Get sorted sessions (most recent first)
  const sessions = Array.from(chatSessions.entries()).sort((a, b) => {
    const aTime = new Date(a[1][0]?.timestamp || 0).getTime();
    const bTime = new Date(b[1][0]?.timestamp || 0).getTime();
    return bTime - aTime;
  });

  sessions.forEach(([chatId, messages]) => {
    if (messages.length === 0) return;

    // Get first message as title
    const firstUserMsg = messages.find((m) => m.role === "user");
    const title = firstUserMsg
      ? firstUserMsg.content.substring(0, 50)
      : "Cuộc trò chuyện";

    const sessionEl = document.createElement("div");
    sessionEl.className = `chat-history-item ${
      currentChatId === chatId ? "active" : ""
    }`;
    sessionEl.onclick = () => loadChatSession(chatId);

    sessionEl.innerHTML = `
            <div class="chat-history-title">${title}${
      title.length >= 50 ? "..." : ""
    }</div>
            <div class="chat-history-actions">
                <button class="delete-btn" onclick="deleteChatSession(event, '${chatId}')">✕</button>
            </div>
        `;

    historyContainer.appendChild(sessionEl);
  });
}

/**
 * Delete a chat session
 */
function deleteChatSession(event, chatId) {
  event.stopPropagation();

  if (confirm("Bạn có chắc chắn muốn xóa cuộc trò chuyện này?")) {
    chatSessions.delete(chatId);

    if (currentChatId === chatId) {
      newChat();
    } else {
      updateChatHistoryUI();
    }

    saveChatHistory();
  }
}

/**
 * Toggle dark mode
 */
function toggleDarkMode() {
  isDarkMode = !isDarkMode;
  document.body.classList.toggle("dark-mode");
  localStorage.setItem(DARK_MODE_STORAGE_KEY, isDarkMode);
}

/**
 * Get chat statistics
 */
function getChatStats() {
  const totalChats = chatSessions.size;
  let totalMessages = 0;

  chatSessions.forEach((messages) => {
    totalMessages += messages.length;
  });

  return {
    totalChats,
    totalMessages,
    averageMessagesPerChat:
      totalChats > 0 ? Math.round(totalMessages / totalChats) : 0,
  };
}

// Export for global access
window.askQuestion = askQuestion;
window.askSuggested = askSuggested;
window.newChat = newChat;
window.toggleDarkMode = toggleDarkMode;
window.handleInputKeyPress = handleInputKeyPress;
window.deleteChatSession = deleteChatSession;
