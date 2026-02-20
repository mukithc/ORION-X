const messagesEl = document.getElementById('messages');
const typingEl = document.getElementById('typing');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model');
const clearBtn = document.getElementById('clear-btn');

// Load models on startup
async function loadModels() {
  try {
    const res = await fetch('/api/models');
    const data = await res.json();
    modelSelect.innerHTML = data.models.map(m => 
      `<option value="${m}">${m}</option>`
    ).join('');
    if (data.default && data.models.includes(data.default)) {
      modelSelect.value = data.default;
    }
  } catch (e) {
    modelSelect.innerHTML = '<option value="llama2:latest">llama2:latest</option>';
  }
}

// Chat history for API
let history = [];

function addMessage(role, content) {
  const msg = document.createElement('div');
  msg.className = `message ${role}`;
  const avatar = role === 'user' ? 'U' : 'X';
  msg.innerHTML = `
    <div class="message-avatar">${avatar}</div>
    <div class="message-content">${escapeHtml(content)}</div>
  `;
  messagesEl.appendChild(msg);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML.replace(/\n/g, '<br>');
}

function updateLastMessage(content) {
  const last = messagesEl.querySelector('.message.assistant:last-child .message-content');
  if (last) last.innerHTML = escapeHtml(content);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

let abortController = null;

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  abortController?.abort();
  abortController = new AbortController();

  input.value = '';
  input.style.height = 'auto';

  addMessage('user', text);
  history.push({ role: 'user', content: text });

  typingEl.style.display = 'flex';
  sendBtn.disabled = true;
  sendBtn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12"/></svg>';
  sendBtn.title = 'Stop';

  const assistantMsg = { role: 'assistant', content: '' };
  addMessage('assistant', '');
  history.push(assistantMsg);

  let fullContent = '';
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        model: modelSelect.value,
        history: history.slice(0, -1),
      }),
      signal: abortController.signal,
    });

    if (!res.ok) throw new Error(res.statusText);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let fullContent = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n');
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.content) {
              fullContent += data.content;
              updateLastMessage(fullContent);
            }
          } catch (_) {}
        }
      }
    }

    assistantMsg.content = fullContent;
  } catch (e) {
    if (e.name === 'AbortError') {
      const stopped = fullContent ? fullContent + '\n\n[Stopped]' : '[Stopped]';
      updateLastMessage(stopped);
      assistantMsg.content = stopped;
    } else {
      updateLastMessage(`Error: ${e.message}. Is Ollama running? Try: ollama serve`);
      history.pop();
    }
  } finally {
    typingEl.style.display = 'none';
    sendBtn.disabled = false;
    sendBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>';
    sendBtn.title = 'Send';
  }
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  if (sendBtn.title === 'Stop') {
    abortController?.abort();
  } else {
    sendMessage();
  }
});

// Auto-resize textarea
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 120) + 'px';
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

clearBtn.addEventListener('click', () => {
  messagesEl.innerHTML = '';
  history = [];
});

loadModels();
