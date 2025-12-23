import React from 'react';
import './Sidebar.css';

interface Notebook {
  id: string;
  name: string;
  count: number;
  icon: string;
}

interface SidebarProps {
  notebooks: Notebook[];
  selectedNotebook: string;
  onSelectNotebook: (notebookId: string) => void;
  onAddNewNotebook: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  notebooks,
  selectedNotebook,
  onSelectNotebook,
  onAddNewNotebook
}) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon">🎓</div>
          <div className="logo-text">NotebookLM MQL</div>
        </div>
        <button className="new-notebook-btn" onClick={onAddNewNotebook}>
          <span className="material-icons-outlined">add</span>
          New Notebook
        </button>
      </div>
      
      <div className="notebooks-section">
        <div className="section-title">Your Notebooks</div>
        {notebooks.map((notebook) => (
          <div
            key={notebook.id}
            className={`notebook-item ${selectedNotebook === notebook.id ? 'active' : ''}`}
            onClick={() => onSelectNotebook(notebook.id)}
          >
            <div className="notebook-icon">{notebook.icon}</div>
            <div className="notebook-name">{notebook.name}</div>
            <div className="notebook-count">{notebook.count}</div>
          </div>
        ))}
        <div className="notebook-item" onClick={onAddNewNotebook}>
          <div className="notebook-icon">➕</div>
          <div className="notebook-name">Add New Notebook</div>
          <div className="notebook-count">+</div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;