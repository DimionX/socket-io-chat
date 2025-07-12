document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const form = document.getElementById('chat-form');
    const input = document.getElementById('msg-input');
    const messages = document.getElementById('messages');
    const typingEl = document.getElementById('typing');
    const fileInput = document.getElementById('file-input');
    const attachBtn = document.getElementById('attach-btn');
    const chatId = window.location.pathname.split('/').pop();
    let typingTimer = null;
    let isTyping = false;
    let lastMsg = { text: null, time: null };

    // Format time as HH:MM:SS
    const fmtTime = (utcString) => {
        const date = new Date(utcString);
        return date.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false,
        });
    };

    // Add message to chat window
    const addMessage = (content, isUser, time = fmtTime(Date.now())) => {
        const msgEl = document.createElement('div');
        msgEl.className = `msg msg--${isUser ? 'user' : 'other'}`;

        if (typeof content === 'string' && content.startsWith('data:image')) {
            const img = document.createElement('img');
            img.src = content;
            img.className = 'chat-image';
            img.alt = 'Image';
            img.loading = 'lazy';
            msgEl.append(img);
        } else {
            msgEl.textContent = content;
        }

        const tm = document.createElement('time');
        tm.dateTime = new Date().toISOString();
        tm.textContent = time;
        msgEl.append(tm);

        messages.append(msgEl);
        messages.scrollTop = messages.scrollHeight;
    };

    // Send message to server
    const sendMessage = (message) => {
        const time = fmtTime(Date.now());
        addMessage(message, true, time);
        lastMsg = { text: message, time };
        socket.emit('send_message', { chat_id: chatId, message, timestamp: time });
    };

    // Socket event handlers
    socket.on('connect', () => {
        socket.emit('join', { chat_id: chatId });
        console.log('Connected');
    });

    socket.on('receive_message', ({ message, timestamp }) => {
        if (message === lastMsg.text && timestamp === lastMsg.time) return;
        const localTime = fmtTime(timestamp);
        addMessage(message, false, localTime);
    });

    socket.on('show_typing', () => {
        typingEl.textContent = `User is typing…`;
        typingEl.style.opacity = '1';
    });

    socket.on('hide_typing', () => {
        typingEl.style.opacity = '0';
    });

    // Debounce utility function
    const debounce = (fn, delay) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => fn(...args), delay);
        };
    };

    // Typing indicator with debounce
    input.addEventListener('input', debounce(() => {
        if (!isTyping) {
            socket.emit('typing', { chat_id: chatId });
            isTyping = true;
        }
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            socket.emit('stop_typing', { chat_id: chatId });
            isTyping = false;
        }, 1500);
    }, 250));

    // Send text message
    form.addEventListener('submit', e => {
        e.preventDefault();
        const msg = input.value.trim();
        if (msg) sendMessage(msg);
        input.value = '';
        input.focus();
    });

    // Handle image upload
    const handleImageFile = file => {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        const reader = new FileReader();
        reader.onload = () => sendMessage(reader.result);
        reader.readAsDataURL(file);
    };

    attachBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
        if (fileInput.files[0]) handleImageFile(fileInput.files[0]);
        fileInput.value = '';
    });

    document.addEventListener('paste', e => {
        const item = [...e.clipboardData.items].find(i => i.type.startsWith('image/'));
        if (item) handleImageFile(item.getAsFile());
    });

    // Image preview modal on click
    messages.addEventListener('click', e => {
        if (e.target.matches('.chat-image')) {
            const modal = document.createElement('div');
            modal.className = 'modal';
            const img = e.target.cloneNode();
            img.style.maxWidth = img.style.maxHeight = '90%';
            modal.append(img);
            modal.addEventListener('click', () => modal.remove());
            document.body.append(modal);
        }
    });

    // Hide preview modal
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            document.querySelector('.modal')?.remove();
        }
    });

    // Autofocus on input when page loads
    input.focus();
});
