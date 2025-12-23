import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import DocumentsPanel from './DocumentsPanel';
import ChatInterface from './ChatInterface';
import './DebateInterface.css';

interface Notebook {
  id: string;
  name: string;
  count: number;
  icon: string;
}

interface Document {
  name: string;
  size: number;
  type: string;
}

const DebateInterface: React.FC = () => {
  const [notebooks, setNotebooks] = useState<Notebook[]>([
    { id: 'main', name: 'Main Debate Notebook', count: 3, icon: '📚' },
    { id: 'research', name: 'Research Papers', count: 7, icon: '🔬' },
    { id: 'studies', name: 'Course Materials', count: 12, icon: '📖' }
  ]);
  
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedNotebook, setSelectedNotebook] = useState<string>('main');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch('/api/documents');
      const data = await response.json();
      if (data.success) {
        setDocuments(data.documents);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleSelectNotebook = (notebookId: string) => {
    setSelectedNotebook(notebookId);
  };

  const handleAddNewNotebook = () => {
    const notebookName = prompt('Enter a name for your new notebook:');
    if (!notebookName || notebookName.trim() === '') {
      addStatusMessage('Notebook name cannot be empty', 'error');
      return;
    }

    const newNotebook: Notebook = {
      id: notebookName.trim().toLowerCase().replace(/\s+/g, '-'),
      name: notebookName.trim(),
      count: 0,
      icon: '📝'
    };

    setNotebooks([...notebooks, newNotebook]);
    setSelectedNotebook(newNotebook.id);
    addStatusMessage(`New notebook "${notebookName.trim()}" created successfully!`, 'success');
  };

  const addStatusMessage = (content: string, type: 'loading' | 'success' | 'error') => {
    // This will be handled by the ChatInterface component
    console.log(`${type}: ${content}`);
  };

  return (
    <div className="debate-interface">
      {/* Sidebar */}
      <Sidebar 
        notebooks={notebooks}
        selectedNotebook={selectedNotebook}
        onSelectNotebook={handleSelectNotebook}
        onAddNewNotebook={handleAddNewNotebook}
      />

      {/* Main Content */}
      <div className="main-content">
        {/* Main Header */}
        <div className="main-header">
          <div>
            <div className="main-title">
              <span className="material-icons-outlined">smart_toy</span>
              AI Debate Generator
            </div>
            <div className="main-subtitle">
              Generate structured academic debates from your documents
            </div>
          </div>
          <div className="header-actions">
            <button className="header-btn" onClick={fetchDocuments}>
              <span className="material-icons-outlined">refresh</span>
              Refresh
            </button>
            <button className="header-btn primary" onClick={() => {}}>
              <span className="material-icons-outlined">download</span>
              Export
            </button>
          </div>
        </div>

        {/* Content Area */}
        <div className="content-area">
          {/* Documents Panel */}
          <DocumentsPanel 
            documents={documents}
            onRefresh={fetchDocuments}
          />

          {/* Chat Interface */}
          <div className="chat-container" ref={chatContainerRef}>
            <ChatInterface 
              isGenerating={isGenerating}
              onGenerateDebate={(topic) => {}}
              onStatusMessage={addStatusMessage}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default DebateInterface;