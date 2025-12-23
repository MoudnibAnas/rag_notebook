import React, { useState } from 'react';
import './DocumentsPanel.css';

interface Document {
  name: string;
  size: number;
  type: string;
}

interface DocumentsPanelProps {
  documents: Document[];
  onRefresh: () => void;
}

const DocumentsPanel: React.FC<DocumentsPanelProps> = ({ documents, onRefresh }) => {
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState<boolean>(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    setIsUploading(true);
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout

      const response = await fetch('/api/upload', {
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
        alert(data.message);
        onRefresh();
      } else {
        alert('Upload failed: ' + data.error);
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        alert('Upload timed out. Please try uploading fewer files.');
      } else if (error.name === 'TypeError') {
        alert('Network error during upload. Please check your connection.');
      } else {
        alert('Upload error: ' + error.message);
      }
      console.error('Upload error:', error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSelectDocument = (docName: string) => {
    setSelectedDocument(docName);
    alert('Selected document: ' + docName);
  };

  const formatFileSize = (bytes: number): string => {
    return (bytes / (1024 * 1024)).toFixed(2);
  };

  return (
    <div className="documents-panel">
      <div className="panel-title">
        <span className="material-icons-outlined">description</span>
        Source Documents
      </div>
      
      <div id="documents-list">
        {documents.length === 0 ? (
          <div style={{ color: 'var(--text-tertiary)', padding: '16px' }}>
            No documents found. Upload PDFs to get started.
          </div>
        ) : (
          documents.map((doc, index) => (
            <div
              key={index}
              className={`document-item ${selectedDocument === doc.name ? 'selected' : ''}`}
              onClick={() => handleSelectDocument(doc.name)}
            >
              <div className="document-name">{doc.name}</div>
              <div className="document-meta">PDF • {formatFileSize(doc.size)} MB</div>
            </div>
          ))
        )}
      </div>

      <div className="upload-section">
        <input
          type="file"
          id="file-input"
          accept=".pdf"
          multiple
          onChange={handleFileUpload}
          disabled={isUploading}
          style={{ width: '100%', padding: '8px', border: '1px solid var(--border-color)', borderRadius: 'var(--border-radius)', background: 'white' }}
        />
        <button
          className="header-btn upload-btn"
          onClick={() => document.getElementById('file-input')?.click()}
          disabled={isUploading}
        >
          <span className="material-icons-outlined">upload</span>
          Upload PDFs
        </button>
        <button className="header-btn refresh-btn" onClick={onRefresh}>
          <span className="material-icons-outlined">refresh</span>
          Refresh Documents
        </button>
      </div>
    </div>
  );
};

export default DocumentsPanel;