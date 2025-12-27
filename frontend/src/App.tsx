import './App.css';
import { BrowserRouter as Router, Routes } from 'react-router-dom';
// import NotebookLM from './components/NotebookLM';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          {/* <Route path="/" element={<NotebookLM />} /> */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;