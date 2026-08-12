/**
 * Chatbot AI — Frontend Application
 * Handles chat interaction, UI state, and API communication.
 */

(() => {
    'use strict';

    // --- DOM Elements ---
    const chatMessages = document.getElementById('chatMessages');
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const welcomeScreen = document.getElementById('welcomeScreen');
    const resetBtn = document.getElementById('resetBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const headerStatus = document.getElementById('headerStatus');

    // --- State ---
    let isLoading = false;
    let messageCount = 0;

    // --- Utilities ---

    function getTimeString() {
        return new Date().toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit',
        });
    }

    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /** Simple markdown-like formatting for bot responses */
    function formatBotMessage(text) {
        let formatted = escapeHTML(text);

        // Code blocks (```)
        formatted = formatted.replace(/```(\w*)\n?([\s\S]*?)```/g, (_, lang, code) => {
            return `<pre><code class="language-${lang}">${code.trim()}</code></pre>`;
        });

        // Inline code
        formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

        // Bold
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // Italic
        formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');

        // Line breaks
        formatted = formatted.replace(/\n/g, '<br>');

        return formatted;
    }

    function showToast(message) {
        // Remove existing toast
        const existing = document.querySelector('.toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(() => {
            toast.classList.add('show');
        });

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    }

    // --- Sidebar ---

    function openSidebar() {
        sidebar.classList.add('open');
        sidebarOverlay.classList.add('active');
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        sidebarOverlay.classList.remove('active');
    }

    menuBtn.addEventListener('click', openSidebar);
    sidebarClose.addEventListener('click', closeSidebar);
    sidebarOverlay.addEventListener('click', closeSidebar);

    // --- Textarea Auto-Resize ---

    messageInput.addEventListener('input', () => {
        // Enable/disable send button
        sendBtn.disabled = !messageInput.value.trim();

        // Auto resize
        messageInput.style.height = 'auto';
        const maxHeight = 150;
        messageInput.style.height = Math.min(messageInput.scrollHeight, maxHeight) + 'px';
    });

    // Submit on Enter (Shift+Enter for new line)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled && !isLoading) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    // --- Message Rendering ---

    function hideWelcomeScreen() {
        if (welcomeScreen) {
            welcomeScreen.style.animation = 'fadeOut 0.25s ease-out forwards';
            setTimeout(() => {
                welcomeScreen.remove();
            }, 250);
        }
    }

    function addMessage(role, content) {
        messageCount++;
        const isUser = role === 'user';

        const row = document.createElement('div');
        row.className = `message-row ${isUser ? 'user' : 'bot'}`;
        row.id = `msg-${messageCount}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = isUser ? '🧑' : 'AI';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        if (isUser) {
            bubble.textContent = content;
        } else {
            bubble.innerHTML = formatBotMessage(content);
        }

        const time = document.createElement('div');
        time.className = 'message-time';
        time.textContent = getTimeString();

        contentDiv.appendChild(bubble);
        contentDiv.appendChild(time);
        row.appendChild(avatar);
        row.appendChild(contentDiv);

        chatMessages.appendChild(row);
        scrollToBottom();

        return row;
    }

    function addTypingIndicator() {
        const row = document.createElement('div');
        row.className = 'message-row bot';
        row.id = 'typing-indicator';

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = 'AI';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        const typing = document.createElement('div');
        typing.className = 'typing-indicator';
        typing.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';

        bubble.appendChild(typing);
        contentDiv.appendChild(bubble);
        row.appendChild(avatar);
        row.appendChild(contentDiv);

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // --- API Communication ---

    async function sendMessage(text) {
        if (isLoading || !text.trim()) return;

        isLoading = true;
        headerStatus.textContent = 'Sedang mengetik...';
        headerStatus.style.color = 'var(--warning)';
        sendBtn.disabled = true;

        // Hide welcome screen & show user message
        hideWelcomeScreen();
        addMessage('user', text);

        // Show typing indicator
        addTypingIndicator();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text }),
            });

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
            }

            const data = await res.json();
            removeTypingIndicator();
            addMessage('bot', data.reply);

        } catch (err) {
            removeTypingIndicator();
            addMessage('bot', `⚠️ Gagal menghubungi server: ${err.message}`);
            console.error('Chat error:', err);
        } finally {
            isLoading = false;
            headerStatus.textContent = 'Online';
            headerStatus.style.color = '';
            sendBtn.disabled = !messageInput.value.trim();
        }
    }

    async function resetConversation() {
        try {
            const res = await fetch('/api/reset', { method: 'POST' });
            if (!res.ok) throw new Error('Reset failed');

            // Clear UI
            chatMessages.innerHTML = '';
            messageCount = 0;

            // Re-add welcome screen
            const welcome = document.createElement('div');
            welcome.className = 'welcome-screen';
            welcome.id = 'welcomeScreen';
            welcome.innerHTML = `
                <div class="welcome-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="url(#welcomeGrad2)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <defs>
                            <linearGradient id="welcomeGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" style="stop-color:#818cf8"/>
                                <stop offset="100%" style="stop-color:#c084fc"/>
                            </linearGradient>
                        </defs>
                        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                        <path d="M2 17l10 5 10-5"/>
                        <path d="M2 12l10 5 10-5"/>
                    </svg>
                </div>
                <h2>Halo! Saya Asisten AI Anda 👋</h2>
                <p>Saya siap membantu menjawab pertanyaan, berdiskusi, atau sekadar ngobrol santai.</p>
                <div class="suggestion-chips">
                    <button class="chip" data-message="Ceritakan tentang dirimu">💬 Ceritakan tentang dirimu</button>
                    <button class="chip" data-message="Apa saja yang bisa kamu bantu?">🤔 Apa yang bisa kamu bantu?</button>
                    <button class="chip" data-message="Jelaskan cara kerja AI secara sederhana">🧠 Jelaskan cara kerja AI</button>
                </div>
            `;
            chatMessages.appendChild(welcome);
            bindChipEvents();

            showToast('🧹 Percakapan telah di-reset');

        } catch (err) {
            showToast('❌ Gagal mereset percakapan');
            console.error('Reset error:', err);
        }
    }

    // --- Event Handlers ---

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();
        if (!text) return;

        messageInput.value = '';
        messageInput.style.height = 'auto';
        sendBtn.disabled = true;

        sendMessage(text);
    });

    resetBtn.addEventListener('click', () => {
        resetConversation();
    });

    newChatBtn.addEventListener('click', () => {
        resetConversation();
        closeSidebar();
    });

    // --- Suggestion Chips ---

    function bindChipEvents() {
        document.querySelectorAll('.chip[data-message]').forEach((chip) => {
            chip.addEventListener('click', () => {
                const msg = chip.getAttribute('data-message');
                if (msg && !isLoading) {
                    sendMessage(msg);
                }
            });
        });
    }

    bindChipEvents();

    // --- CSS fadeOut animation (injected) ---
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-10px); }
        }
    `;
    document.head.appendChild(style);

    // --- Focus input on load ---
    messageInput.focus();

})();
