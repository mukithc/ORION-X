const messagesEl = document.getElementById('messages');
const typingEl = document.getElementById('typing');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model');

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

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = 'auto';

  addMessage('user', text);
  history.push({ role: 'user', content: text });

  typingEl.style.display = 'flex';
  sendBtn.disabled = true;

  const assistantMsg = { role: 'assistant', content: '' };
  addMessage('assistant', '');
  history.push(assistantMsg);

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        model: modelSelect.value,
        history: history.slice(0, -1),
      }),
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
    updateLastMessage(`Error: ${e.message}. Is Ollama running? Try: ollama serve`);
    history.pop();
  } finally {
    typingEl.style.display = 'none';
    sendBtn.disabled = false;
  }
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  sendMessage();
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

loadModels();
