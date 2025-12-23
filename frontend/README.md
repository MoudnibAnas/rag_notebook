# RAG Debate Generator - React Frontend

This is the React frontend for the RAG Debate Generator application, providing a modern, interactive interface for generating structured academic debates from uploaded documents.

## Features

- **Notebook Management**: Create and manage multiple notebooks for organizing debates
- **Document Upload**: Upload PDF documents for analysis and debate generation
- **Real-time Chat Interface**: Interactive chat interface for generating debates
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, NotebookLM-inspired design

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and development server
- **React Router**: Client-side routing
- **CSS-in-JS**: Component-scoped styling with CSS modules

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd local_rag_debate/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Sidebar.tsx         # Notebook management sidebar
│   │   ├── DocumentsPanel.tsx  # Document upload and management
│   │   ├── ChatInterface.tsx   # Main chat interface
│   │   └── DebateInterface.tsx # Main application container
│   ├── App.tsx                 # Main App component with routing
│   ├── main.tsx               # Application entry point
│   └── index.css              # Global styles
├── package.json               # Dependencies and scripts
├── vite.config.ts             # Vite configuration
└── index.html                 # HTML template
```

## API Integration

The frontend communicates with the Flask backend via the following endpoints:

- `GET /api/documents` - Get list of uploaded documents
- `POST /api/upload` - Upload new PDF documents
- `POST /api/generate` - Generate debates from topics
- `POST /api/create_database` - Create/update the RAG database

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run linting (if configured)

### Environment Configuration

The frontend is configured to proxy API requests to the Flask backend running on `http://localhost:5000`. This is configured in `vite.config.ts`.

## Backend Requirements

Make sure the Flask backend is running before starting the frontend:

1. Navigate to the project root:
   ```bash
   cd local_rag_debate
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. The backend will be available at `http://localhost:5000`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - see LICENSE file for details.