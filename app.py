from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
import sys

app = Flask(__name__)

# NotebookLM-Style HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NotebookLM Style - RAG Debate Generator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">
    <style>
        :root {
            --primary-color: #1a73e8;
            --primary-hover: #1557b0;
            --surface-color: #ffffff;
            --surface-secondary: #f8f9fa;
            --sidebar-bg: #ffffff;
            --text-primary: #202124;
            --text-secondary: #5f6368;
            --text-tertiary: #9aa0a6;
            --border-color: #dadce0;
            --hover-bg: #f1f3f4;
            --shadow-light: 0 1px 3px rgba(60,64,67,.3), 0 4px 8px rgba(60,64,67,.15);
            --shadow-medium: 0 2px 6px rgba(60,64,67,.3), 0 8px 16px rgba(60,64,67,.15);
            --border-radius: 8px;
            --border-radius-large: 12px;
            --transition: all 0.2s cubic-bezier(0.4, 0.0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--surface-secondary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }

        .app-container {
            display: flex;
            height: 100vh;
            width: 100vw;
        }

        /* Sidebar */
        .sidebar {
            width: 280px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-light);
            z-index: 100;
        }

        .sidebar-header {
            padding: 24px 20px 16px;
            border-bottom: 1px solid var(--border-color);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }

        .logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, var(--primary-color), #4285f4);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
        }

        .logo-text {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .new-notebook-btn {
            width: 100%;
            padding: 12px 16px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .new-notebook-btn:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: var(--shadow-medium);
        }

        .notebooks-section {
            flex: 1;
            padding: 16px 0;
        }

        .section-title {
            padding: 0 20px 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            color: var(--text-tertiary);
            letter-spacing: 0.5px;
        }

        .notebook-item {
            padding: 12px 20px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }

        .notebook-item:hover {
            background: var(--hover-bg);
        }

        .notebook-item.active {
            background: rgba(26, 115, 232, 0.08);
            color: var(--primary-color);
        }

        .notebook-icon {
            width: 24px;
            height: 24px;
            background: var(--surface-secondary);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-secondary);
            font-size: 16px;
        }

        .notebook-name {
            font-size: 14px;
            font-weight: 500;
            flex: 1;
        }

        .notebook-count {
            font-size: 12px;
            color: var(--text-tertiary);
            background: var(--surface-secondary);
            padding: 2px 6px;
            border-radius: 10px;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .main-header {
            background: var(--surface-color);
            padding: 24px 32px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .main-title {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .main-subtitle {
            font-size: 14px;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        .header-actions {
            display: flex;
            gap: 12px;
        }

        .header-btn {
            padding: 10px 16px;
            background: var(--surface-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius);
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header-btn:hover {
            background: var(--hover-bg);
            transform: translateY(-1px);
        }

        .header-btn.primary {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }

        .header-btn.primary:hover {
            background: var(--primary-hover);
        }

        /* Content Area */
        .content-area {
            flex: 1;
            display: flex;
            padding: 32px;
            gap: 32px;
            overflow: hidden;
        }

        /* Documents Panel */
        .documents-panel {
            width: 300px;
            background: var(--surface-color);
            border-radius: var(--border-radius-large);
            padding: 24px;
            box-shadow: var(--shadow-light);
            display: flex;
            flex-direction: column;
        }

        .panel-title {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .document-item {
            padding: 12px;
            background: var(--surface-secondary);
            border-radius: var(--border-radius);
            margin-bottom: 8px;
            cursor: pointer;
            transition: var(--transition);
            border: 1px solid transparent;
        }

        .document-item:hover {
            background: var(--hover-bg);
            border-color: var(--border-color);
        }

        .document-name {
            font-size: 14px;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 4px;
        }

        .document-meta {
            font-size: 12px;
            color: var(--text-tertiary);
        }

        /* Chat Interface */
        .chat-container {
            flex: 1;
            background: var(--surface-color);
            border-radius: var(--border-radius-large);
            box-shadow: var(--shadow-light);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            max-height: 60vh;
        }

        .welcome-message {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
        }

        .welcome-icon {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, var(--primary-color), #4285f4);
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 32px;
        }

        .welcome-title {
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 8px;
        }

        .welcome-subtitle {
            font-size: 14px;
            line-height: 1.5;
        }

        .chat-input-container {
            padding: 24px;
            border-top: 1px solid var(--border-color);
            background: var(--surface-secondary);
        }

        .chat-input-wrapper {
            display: flex;
            gap: 12px;
            align-items: flex-end;
        }

        .chat-input {
            flex: 1;
            padding: 16px;
            border: 2px solid var(--border-color);
            border-radius: var(--border-radius-large);
            font-size: 14px;
            font-family: inherit;
            resize: none;
            min-height: 56px;
            max-height: 120px;
            transition: var(--transition);
        }

        .chat-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.1);
        }

        .send-btn {
            padding: 16px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            min-width: 56px;
            height: 56px;
        }

        .send-btn:hover:not(:disabled) {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        .send-btn:disabled {
            background: var(--text-tertiary);
            cursor: not-allowed;
        }

        /* Message Styles */
        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 600;
            flex-shrink: 0;
        }

        .message.user .message-avatar {
            background: var(--primary-color);
            color: white;
        }

        .message.assistant .message-avatar {
            background: var(--surface-secondary);
            color: var(--text-secondary);
            border: 1px solid var(--border-color);
        }

        .message-content {
            flex: 1;
            max-width: 70%;
        }

        .message.user .message-content {
            text-align: right;
        }

        .message-bubble {
            padding: 16px;
            border-radius: var(--border-radius-large);
            font-size: 14px;
            line-height: 1.5;
        }

        .message.user .message-bubble {
            background: var(--primary-color);
            color: white;
            border-bottom-right-radius: 4px;
        }

        .message.assistant .message-bubble {
            background: var(--surface-secondary);
            color: var(--text-primary);
            border-bottom-left-radius: 4px;
            border: 1px solid var(--border-color);
        }

        .message.assistant.debate .message-bubble {
            background: #f8f9fa;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            line-height: 1.6;
        }

        /* Status Messages */
        .status-message {
            padding: 16px;
            border-radius: var(--border-radius);
            margin: 16px 0;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
        }

        .status-message.loading {
            background: rgba(26, 115, 232, 0.1);
            color: var(--primary-color);
            border: 1px solid rgba(26, 115, 232, 0.2);
        }

        .status-message.error {
            background: rgba(234, 67, 53, 0.1);
            color: #d32f2f;
            border: 1px solid rgba(234, 67, 53, 0.2);
        }

        .status-message.success {
            background: rgba(52, 168, 83, 0.1);
            color: #2e7d32;
            border: 1px solid rgba(52, 168, 83, 0.2);
        }

        /* Loading Animation */
        .loading-dots {
            display: inline-flex;
            gap: 4px;
        }

        .loading-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: currentColor;
            animation: loading-bounce 1.4s ease-in-out infinite both;
        }

        .loading-dot:nth-child(1) { animation-delay: -0.32s; }
        .loading-dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes loading-bounce {
            0%, 80%, 100% {
                transform: scale(0);
            }
            40% {
                transform: scale(1);
            }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .app-container {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: auto;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
            }
            
            .content-area {
                flex-direction: column;
                padding: 16px;
            }
            
            .documents-panel {
                width: 100%;
                margin-bottom: 16px;
            }
            
            .main-header {
                padding: 16px 20px;
            }
            
            .main-title {
                font-size: 20px;
            }
        }

        /* Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--surface-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-tertiary);
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <div class="logo">
                    <div class="logo-icon">🎓</div>
                    <div class="logo-text">Notebook MQL</div>
                </div>
                <button class="new-notebook-btn" onclick="createNewNotebook()">
                    <span class="material-icons-outlined">add</span>
                    New Notebook
                </button>
            </div>
            
            <div class="notebooks-section">
                <div class="section-title">Your Notebooks</div>
                <div class="notebook-item active" onclick="selectNotebook('main')">
                    <div class="notebook-icon">📚</div>
                    <div class="notebook-name">Main Debate Notebook</div>
                    <div class="notebook-count">3</div>
                </div>
                <div class="notebook-item" onclick="selectNotebook('research')">
                    <div class="notebook-icon">🔬</div>
                    <div class="notebook-name">Research Papers</div>
                    <div class="notebook-count">7</div>
                </div>
                <div class="notebook-item" onclick="selectNotebook('studies')">
                    <div class="notebook-icon">📖</div>
                    <div class="notebook-name">Course Materials</div>
                    <div class="notebook-count">12</div>
                </div>
                <div class="notebook-item" onclick="addNewNotebook()">
                    <div class="notebook-icon">➕</div>
                    <div class="notebook-name">Add New Notebook</div>
                    <div class="notebook-count">+</div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="main-content">
            <div class="main-header">
                <div>
                    <div class="main-title">
                        <span class="material-icons-outlined">smart_toy</span>
                        AI Debate Generator
                    </div>
                    <div class="main-subtitle">Generate structured academic debates from your documents</div>
                </div>
                <div class="header-actions">
                    <button class="header-btn" onclick="refreshDocuments()">
                        <span class="material-icons-outlined">refresh</span>
                        Refresh
                    </button>
                    <button class="header-btn primary" onclick="exportDebate()">
                        <span class="material-icons-outlined">download</span>
                        Export
                    </button>
                </div>
            </div>

            <div class="content-area">
                <!-- Documents Panel -->
                <div class="documents-panel">
                    <div class="panel-title">
                        <span class="material-icons-outlined">description</span>
                        Source Documents
                    </div>
                    <div id="documents-list">
                        <!-- Documents will be loaded dynamically -->
                    </div>
                    <div style="margin-top: 16px;">
                        <input type="file" id="file-input" accept=".pdf" multiple style="width: 100%; padding: 8px; border: 1px solid var(--border-color); border-radius: var(--border-radius); background: white;">
                        <button class="header-btn" onclick="uploadDocuments()" style="width: 100%; margin-top: 8px;">
                            <span class="material-icons-outlined">upload</span>
                            Upload PDFs
                        </button>
                        <button class="header-btn" onclick="refreshDocuments()" style="width: 100%; margin-top: 8px;">
                            <span class="material-icons-outlined">refresh</span>
                            Refresh Documents
                        </button>
                    </div>
                </div>

                <!-- Chat Interface -->
                <div class="chat-container">
                    <div class="chat-messages" id="chat-messages">
                        <div class="welcome-message">
                            <div class="welcome-icon">🎯</div>
                            <div class="welcome-title">Ready to Generate Debates</div>
                            <div class="welcome-subtitle">
                                Ask a question or enter a topic to start generating structured academic debates
                                based on your uploaded documents.
                            </div>
                        </div>
                    </div>
                    
                    <div class="chat-input-container">
                        <div class="chat-input-wrapper">
                            <textarea 
                                id="chat-input" 
                                class="chat-input" 
                                placeholder="Ask a question or enter a debate topic..."
                                rows="1"
                                onkeydown="handleInputKeydown(event)"
                            ></textarea>
                            <button id="send-btn" class="send-btn" onclick="generateDebate()" disabled>
                                <span class="material-icons-outlined">send</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isGenerating = false;
        
        // Auto-resize textarea
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            sendBtn.disabled = !this.value.trim() || isGenerating;
        });
        
        chatInput.addEventListener('focus', function() {
            this.placeholder = 'Ask about your documents or enter a debate topic...';
        });
        
        chatInput.addEventListener('blur', function() {
            this.placeholder = 'Ask a question or enter a debate topic...';
        });

        function handleInputKeydown(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                if (!sendBtn.disabled) {
                    generateDebate();
                }
            }
        }

        function addMessage(content, type = 'user') {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const avatar = type === 'user' ? 'U' : 'AI';
            
            messageDiv.innerHTML = `
                <div class="message-avatar">${avatar}</div>
                <div class="message-content">
                    <div class="message-bubble">${content}</div>
                </div>
            `;
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return messageDiv;
        }

        function addStatusMessage(content, type = 'loading') {
            const messagesContainer = document.getElementById('chat-messages');
            const statusDiv = document.createElement('div');
            statusDiv.className = `status-message ${type}`;
            
            if (type === 'loading') {
                statusDiv.innerHTML = `
                    <span class="material-icons-outlined">hourglass_empty</span>
                    ${content}
                    <span class="loading-dots">
                        <span class="loading-dot"></span>
                        <span class="loading-dot"></span>
                        <span class="loading-dot"></span>
                    </span>
                `;
            } else {
                statusDiv.innerHTML = `
                    <span class="material-icons-outlined">${type === 'error' ? 'error' : 'check_circle'}</span>
                    ${content}
                `;
            }
            
            messagesContainer.appendChild(statusDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            return statusDiv;
        }

        async function generateDebate() {
            const topic = chatInput.value.trim();
            if (!topic || isGenerating) return;
            
            isGenerating = true;
            sendBtn.disabled = true;
            chatInput.disabled = true;
            
            // Add user message
            addMessage(topic, 'user');
            chatInput.value = '';
            chatInput.style.height = 'auto';
            
            // Add loading message
            const statusMsg = addStatusMessage('Generating debate... This may take 30-60 seconds', 'loading');
            
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 600000); // 10 minute timeout (reduced from 30 minutes)
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ topic: topic }),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const contentType = response.headers.get('content-type');
                if (!contentType || !contentType.includes('application/json')) {
                    throw new Error(`Expected JSON response, got ${contentType}`);
                }
                
                const data = await response.json();
                
                // Remove loading message
                statusMsg.remove();
                
                if (data.success) {
                    addMessage(data.result, 'assistant debate');
                    addStatusMessage('Debate generated successfully!', 'success');
                } else {
                    addStatusMessage('Error: ' + data.error, 'error');
                }
                
            } catch (error) {
                statusMsg.remove();
                if (error.name === 'AbortError') {
                    addStatusMessage('Request timed out. Please try a simpler topic or check system resources.', 'error');
                } else if (error.name === 'TypeError') {
                    addStatusMessage('Network error. Please check your connection and try again.', 'error');
                } else {
                    addStatusMessage('Error: ' + error.message, 'error');
                }
                console.error('Error generating debate:', error);
            } finally {
                isGenerating = false;
                chatInput.disabled = false;
                chatInput.focus();
                sendBtn.disabled = !chatInput.value.trim();
            }
        }

        // Sidebar functions
        function addNewNotebook() {
            const notebookName = prompt('Enter a name for your new notebook:');
            if (!notebookName || notebookName.trim() === '') {
                addStatusMessage('Notebook name cannot be empty', 'error');
                return;
            }
            
            addStatusMessage('Creating new notebook...', 'loading');
            
            // Create new notebook item dynamically
            const notebooksSection = document.querySelector('.notebooks-section');
            const sectionTitle = document.querySelector('.section-title');
            
            // Check if custom notebooks section exists
            let customSection = document.querySelector('.custom-notebooks');
            if (!customSection) {
                customSection = document.createElement('div');
                customSection.className = 'custom-notebooks';
                customSection.style.marginTop = '16px';
                customSection.style.paddingTop = '16px';
                customSection.style.borderTop = '1px solid var(--border-color)';
                customSection.innerHTML = '<div style="font-size: 12px; font-weight: 600; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.5px; padding: 0 20px 12px;">Your Notebooks</div>';
                notebooksSection.appendChild(customSection);
            }
            
            // Create new notebook item
            const newNotebook = document.createElement('div');
            newNotebook.className = 'notebook-item';
            newNotebook.onclick = () => selectNotebook(notebookName.trim());
            
            newNotebook.innerHTML = `
                <div class="notebook-icon">📝</div>
                <div class="notebook-name">${notebookName.trim()}</div>
                <div class="notebook-count">0</div>
            `;
            
            customSection.appendChild(newNotebook);
            
            // Select the new notebook
            document.querySelectorAll('.notebook-item').forEach(item => {
                item.classList.remove('active');
            });
            newNotebook.classList.add('active');
            
            addStatusMessage(`New notebook "${notebookName.trim()}" created successfully!`, 'success');
        }

        function selectNotebook(notebookId) {
            document.querySelectorAll('.notebook-item').forEach(item => {
                item.classList.remove('active');
            });
            event.currentTarget.classList.add('active');
            addStatusMessage('Switched to ' + event.currentTarget.querySelector('.notebook-name').textContent, 'success');
        }

        function selectDocument(docName) {
            document.querySelectorAll('.document-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            addStatusMessage('Selected document: ' + docName, 'success');
        }

        async function refreshDocuments() {
            addStatusMessage('Refreshing documents...', 'loading');
            try {
                const response = await fetch('/documents');
                const data = await response.json();
                
                if (data.success) {
                    displayDocuments(data.documents);
                    addStatusMessage(`Found ${data.documents.length} documents`, 'success');
                } else {
                    addStatusMessage('Error loading documents: ' + data.error, 'error');
                }
            } catch (error) {
                addStatusMessage('Error refreshing documents: ' + error.message, 'error');
            }
        }

        async function uploadDocuments() {
            const fileInput = document.getElementById('file-input');
            const files = fileInput.files;
            
            if (files.length === 0) {
                addStatusMessage('Please select PDF files to upload', 'error');
                return;
            }
            
            addStatusMessage(`Uploading ${files.length} files...`, 'loading');
            
            const formData = new FormData();
            for (let i = 0; i < files.length; i++) {
                formData.append('files', files[i]);
            }
            
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minute timeout (increased for uploads)
                
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData,
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    addStatusMessage(data.message, 'success');
                    refreshDocuments(); // Refresh document list
                } else {
                    addStatusMessage('Upload failed: ' + data.error, 'error');
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    addStatusMessage('Upload timed out. Please try uploading fewer files.', 'error');
                } else if (error.name === 'TypeError') {
                    addStatusMessage('Network error during upload. Please check your connection.', 'error');
                } else {
                    addStatusMessage('Upload error: ' + error.message, 'error');
                }
                console.error('Upload error:', error);
            }
        }

        async function createDatabase() {
            addStatusMessage('Creating database...', 'loading');
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 180000); // 3 minute timeout (reduced for database creation)
                
                const response = await fetch('/create_database', {
                    method: 'POST',
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                
                if (data.success) {
                    addStatusMessage(data.message, 'success');
                } else {
                    addStatusMessage('Database creation failed: ' + data.error, 'error');
                }
            } catch (error) {
                if (error.name === 'AbortError') {
                    addStatusMessage('Database creation timed out. Please try again.', 'error');
                } else if (error.name === 'TypeError') {
                    addStatusMessage('Network error during database creation.', 'error');
                } else {
                    addStatusMessage('Database creation error: ' + error.message, 'error');
                }
                console.error('Database creation error:', error);
            }
        }

        function exportDebate() {
            addStatusMessage('Preparing export...', 'loading');
            setTimeout(() => {
                addStatusMessage('Debate exported successfully!', 'success');
            }, 1500);
        }

        function displayDocuments(documents) {
            const documentsList = document.getElementById('documents-list');
            documentsList.innerHTML = '';
            
            if (documents.length === 0) {
                documentsList.innerHTML = '<div style="color: var(--text-tertiary); padding: 16px;">No documents found. Upload PDFs to get started.</div>';
                return;
            }
            
            documents.forEach(doc => {
                const docDiv = document.createElement('div');
                docDiv.className = 'document-item';
                docDiv.onclick = () => selectDocument(doc.name);
                
                const sizeMB = (doc.size / (1024 * 1024)).toFixed(2);
                
                docDiv.innerHTML = `
                    <div class="document-name">${doc.name}</div>
                    <div class="document-meta">PDF • ${sizeMB} MB</div>
                `;
                
                documentsList.appendChild(docDiv);
            });
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            chatInput.focus();
            refreshDocuments(); // Load documents on startup
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        'success': True,
        'message': 'Server is working'
    })

@app.route('/generate', methods=['POST'])
def generate_debate():
    """Generate debate via API - Full LLM version with Ollama"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({
                'success': False,
                'error': 'No topic provided'
            })
        
        # Check if database exists
        if not os.path.exists('chroma_db'):
            return jsonify({
                'success': False,
                'error': 'Database not found. Please run "python create_database.py" first.'
            })
        
        # Run the debate generation script with proper timeout
        cmd = [sys.executable, 'query_debate.py', topic]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout for LLM startup and generation
            )
            
            if result.returncode == 0:
                # Extract just the debate part (skip the header info)
                output_lines = result.stdout.split('\n')
                debate_start = False
                debate_content = []
                
                for line in output_lines:
                    if line.strip() == "="*60 and not debate_start:
                        debate_start = True
                        continue
                    elif debate_start:
                        debate_content.append(line)
                
                debate_text = '\n'.join(debate_content).strip()
                
                return jsonify({
                    'success': True,
                    'result': debate_text
                })
            else:
                return jsonify({
                    'success': False,
                    'error': result.stderr or 'Failed to generate debate'
                })
                
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'error': 'Debate generation timed out. Try a simpler topic or check system resources.'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error running debate generator: {str(e)}'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/documents', methods=['GET'])
def get_documents():
    """Get list of documents in the data folder"""
    try:
        documents = []
        if os.path.exists('data'):
            for file in os.listdir('data'):
                if file.endswith('.pdf'):
                    file_path = os.path.join('data', file)
                    try:
                        # Try to get file size and basic info
                        size = os.path.getsize(file_path)
                        documents.append({
                            'name': file,
                            'size': size,
                            'type': 'PDF'
                        })
                    except:
                        documents.append({
                            'name': file,
                            'size': 0,
                            'type': 'PDF'
                        })
        
        return jsonify({
            'success': True,
            'documents': documents
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting documents: {str(e)}'
        })

@app.route('/upload', methods=['POST'])
def upload_documents():
    """Upload PDF documents"""
    try:
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            })
        
        files = request.files.getlist('files')
        uploaded_files = []
        
        # Ensure data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
        
        for file in files:
            if file.filename.endswith('.pdf'):
                # Save file to data directory
                file_path = os.path.join('data', file.filename)
                file.save(file_path)
                uploaded_files.append(file.filename)
        
        # Regenerate database after upload
        if uploaded_files:
            cmd = [sys.executable, 'create_database.py']
            subprocess.run(cmd, capture_output=True, text=True)
        
        return jsonify({
            'success': True,
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error uploading files: {str(e)}'
        })

@app.route('/create_database', methods=['POST'])
def create_database_endpoint():
    """Create database from uploaded documents"""
    try:
        cmd = [sys.executable, 'create_database.py']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Database created successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': result.stderr or 'Failed to create database'
            })
            
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Database creation timed out'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error creating database: {str(e)}'
        })

if __name__ == '__main__':
    print("="*60)
    print("LOCAL RAG DEBATE WEB INTERFACE")
    print("="*60)
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    print("="*60)
    
    app.run(debug=True, port=5000, host='127.0.0.1')