import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  isDebate?: boolean;
}

interface StatusMessage {
  id: string;
  type: 'loading' | 'success' | 'error';
  content: string;
}

interface ChatInterfaceProps {
  isGenerating: boolean;
  onGenerateDebate: (topic: string) => void;
  onStatusMessage: (content: string, type: 'loading' | 'success' | 'error') => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  isGenerating,
  onGenerateDebate,
  onStatusMessage
}) => {
  const [messages, setMessages] = useState<(Message | StatusMessage)[]>([
    {
      id: 'welcome',
      type: 'assistant',
      content: '',
      isDebate: false
    }
  ]);
  
  const [inputValue, setInputValue] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);
  
  const chatMessagesRef = useRef<HTMLDivElement>(null);
  const chatInputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages]);

  useEffect(() => {
    if (chatInputRef.current) {
      chatInputRef.current.style.height = 'auto';
      chatInputRef.current.style.height = Math.min(chatInputRef.current.scrollHeight, 120) + 'px';
    }
  }, [inputValue]);

  const handleSendMessage = async () => {
    const topic = inputValue.trim();
    if (!topic || isGenerating) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: topic
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(false);

    // Add loading message
    const loadingMessage: StatusMessage = {
      id: 'loading',
      type: 'loading',
      content: 'Generating debate... This may take 30-60 seconds'
    };

    setMessages(prev => [...prev, loadingMessage]);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 600000); // 10 minute timeout

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
      setMessages(prev => prev.filter(msg => msg.id !== 'loading'));

      if (data.success) {
        const debateMessage: Message = {
          id: Date.now().toString(),
          type: 'assistant',
          content: data.result,
          isDebate: true
        };
        setMessages(prev => [...prev, debateMessage]);
        onStatusMessage('Debate generated successfully!', 'success');
      } else {
        const errorMessage: StatusMessage = {
          id: 'error',
          type: 'error',
          content: 'Error: ' + data.error
        };
        setMessages(prev => [...prev, errorMessage]);
      }

    } catch (error) {
      setMessages(prev => prev.filter(msg => msg.id !== 'loading'));
      
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          const timeoutMessage: StatusMessage = {
            id: 'timeout',
            type: 'error',
            content: 'Request timed out. Please try a simpler topic or check system resources.'
          };
          setMessages(prev => [...prev, timeoutMessage]);
        } else if (error.name === 'TypeError') {
          const networkMessage: StatusMessage = {
            id: 'network',
            type: 'error',
            content: 'Network error. Please check your connection and try again.'
          };
          setMessages(prev => [...prev, networkMessage]);
        } else {
          const errorMessage: StatusMessage = {
            id: 'general',
            type: 'error',
            content: 'Error: ' + error.message
          };
          setMessages(prev => [...prev, errorMessage]);
        }
        
        console.error('Error generating debate:', error);
      } else {
        // Handle non-Error objects
        const errorMessage: StatusMessage = {
          id: 'general',
          type: 'error',
          content: 'Error: ' + (error as string || 'Unknown error')
        };
        setMessages(prev => [...prev, errorMessage]);
        console.error('Error generating debate:', error);
      }
    }
  };

  const handleInputKeyDown = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      if (!isGenerating && inputValue.trim()) {
        handleSendMessage();
      }
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(event.target.value);
    setIsTyping(event.target.value.length > 0);
  };

  const handleInputFocus = () => {
    if (chatInputRef.current) {
      chatInputRef.current.placeholder = 'Ask about your documents or enter a debate topic...';
    }
  };

  const handleInputBlur = () => {
    if (chatInputRef.current) {
      chatInputRef.current.placeholder = 'Ask a question or enter a debate topic...';
    }
  };

  const renderMessage = (message: Message | StatusMessage) => {
    if ('isDebate' in message) {
      // It's a message
      return (
        <div key={message.id} className={`message ${message.type}`}>
          <div className="message-avatar">{message.type === 'user' ? 'U' : 'AI'}</div>
          <div className="message-content">
            <div className={`message-bubble ${message.isDebate ? 'debate' : ''}`}>
              {message.content}
            </div>
          </div>
        </div>
      );
    } else {
      // It's a status message
      return (
        <div key={message.id} className={`status-message ${message.type}`}>
          <span className="material-icons-outlined">
            {message.type === 'loading' ? 'hourglass_empty' : 
             message.type === 'error' ? 'error' : 'check_circle'}
          </span>
          {message.content}
          {message.type === 'loading' && (
            <span className="loading-dots">
              <span className="loading-dot"></span>
              <span className="loading-dot"></span>
              <span className="loading-dot"></span>
            </span>
          )}
        </div>
      );
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages" ref={chatMessagesRef}>
        {messages.length === 1 && messages[0].id === 'welcome' ? (
          <div className="welcome-message">
            <div className="welcome-icon">🎯</div>
            <div className="welcome-title">Ready to Generate Debates</div>
            <div className="welcome-subtitle">
              Ask a question or enter a topic to start generating structured academic debates
              based on your uploaded documents.
            </div>
          </div>
        ) : (
          messages.map(renderMessage)
        )}
      </div>
      
      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea 
            ref={chatInputRef}
            className="chat-input"
            placeholder="Ask a question or enter a debate topic..."
            value={inputValue}
            onChange={handleInputChange}
            onFocus={handleInputFocus}
            onBlur={handleInputBlur}
            onKeyDown={handleInputKeyDown}
            rows={1}
            disabled={isGenerating}
          />
          <button 
            className="send-btn" 
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isGenerating}
          >
            <span className="material-icons-outlined">send</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;