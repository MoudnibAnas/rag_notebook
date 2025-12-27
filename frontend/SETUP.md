# React Frontend Setup Guide

This guide will help you set up and run the React frontend for the RAG Debate Generator.

## Prerequisites

- **Node.js** (version 16 or higher)
- **npm** (version 8 or higher) or **yarn**
- **Python** and **Flask backend** running on port 5000

## Quick Start

### 1. Install Dependencies

Navigate to the frontend directory and install dependencies:

```bash
cd local_rag_debate/frontend
npm install
```

Or using yarn:

```bash
cd local_rag_debate/frontend
yarn install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`.

### 3. Start Backend Server

In a separate terminal, navigate to the project root and start the Flask backend:

```bash
python backend_server.py
```

The backend will start on `http://localhost:5000`.

## Project Structure

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── components/           # React components
│   │   ├── Sidebar/          # Notebook sidebar
│   │   ├── DocumentsPanel/   # Document management
│   │   ├── ChatInterface/    # Chat interface
│   │   └── DebateInterface/  # Main container
│   ├── App.tsx              # Main App component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── package.json             # Dependencies
├── vite.config.ts           # Vite configuration
└── tsconfig.json            # TypeScript configuration
```

## Available Scripts

### Development

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

### Production

To build the frontend for production:

```bash
npm run build
```

This will create a `dist/` directory with the built files.

To serve the production build:

```bash
npm run preview
```

## API Endpoints

The frontend communicates with the Flask backend through these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/documents` | Get list of uploaded documents |
| POST | `/api/upload` | Upload PDF documents |
| POST | `/api/generate` | Generate debate from topic |
| POST | `/api/create_database` | Create/update RAG database |

## Environment Variables

No environment variables are required for development. The API proxy is configured in `vite.config.ts` to forward requests to `http://localhost:5000`.

## Troubleshooting

### Port Already in Use

If port 3000 is already in use, Vite will automatically suggest an alternative port.

### Backend Not Running

Make sure the Flask backend is running on port 5000 before starting the frontend. The frontend will show connection errors if the backend is not available.

### CORS Issues

The frontend is configured to proxy API requests to avoid CORS issues. If you encounter CORS errors, check that the backend is running and the proxy configuration in `vite.config.ts` is correct.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Dependencies

### Core Dependencies

- `react` - React library
- `react-dom` - React DOM rendering
- `react-router-dom` - Client-side routing
- `typescript` - Type checking

### Development Dependencies

- `vite` - Build tool and dev server
- `@vitejs/plugin-react` - React plugin for Vite

## License

MIT License - see LICENSE file for details.