# CodexAtlas AI

## The Visual Intelligence Layer For Software Systems

Turn any GitHub repository into an interactive software universe where developers can visually explore architecture, trace data flows, understand dependencies, simulate changes, generate documentation, and onboard themselves without reading hundreds of files.

---

## Features

- **Visual Knowledge Graph** - Transform codebases into interactive dependency maps
- **Story Mode** - Trace business logic through cinematic data flow animations
- **AI Architect** - Ask repository-aware questions with context-aware AI
- **Health Scanner** - Detect dead code, circular dependencies, and code smells
- **Timeline Explorer** - Visual evolution of your software over time
- **Auto Documentation** - Generate comprehensive docs automatically
- **Dependency Explorer** - Visualize file, component, and service relationships
- **Architecture Generator** - Automatically detect and visualize system layers

---

## Tech Stack

### Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Framer Motion
- React Flow
- D3.js
- Zustand (state management)
- React Router

### Backend
- FastAPI
- Python 3.10+
- Tree-sitter (AST parsing)
- NetworkX (graph operations)
- ChromaDB (vector search)

### Deployment
- Frontend: Vercel
- Backend: Railway/Render

---

## Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.10+
- Git

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/codexatlas.git
cd codexatlas
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with your API URL (default: http://localhost:8000)
```

---

## Running the Application

### Start Backend

```bash
cd backend
# Activate virtual environment if not already active
python main.py
```

The backend will run on `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:3000` (or `http://localhost:5173` with Vite)

---

## Usage

### 1. Scan a Repository

1. Open the application in your browser
2. Paste a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Scan Repository"
4. Wait for the analysis to complete (~30-60 seconds)

### 2. Explore Dependencies

- Navigate to the Dependency Explorer
- Interact with the visual graph
- Click nodes to see details
- Use zoom and pan controls

### 3. View Architecture

- Switch to Architecture View
- See automatically detected system layers
- Review architecture metrics

### 4. Ask AI Questions

- Use the AI Architect feature
- Ask repository-specific questions
- Get context-aware answers

---

## API Endpoints

### GitHub
- `POST /api/github/scan` - Scan a GitHub repository

### Parser
- `POST /api/parser/parse` - Parse repository structure

### Graph
- `GET /api/graph/:repoId` - Get knowledge graph

### Architecture
- `GET /api/architecture/:repoId` - Get architecture analysis

### Documentation
- `POST /api/documentation/generate` - Generate documentation

### Health
- `GET /api/health/:repoId` - Analyze repository health

### AI
- `POST /api/ai/ask` - Ask AI questions

---

## Project Structure

```
codexatlas/
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── GalaxyView/
│   │   │   ├── StoryMode/
│   │   │   ├── FlowExplorer/
│   │   │   ├── DependencyMap/
│   │   │   └── ...
│   │   ├── pages/           # Page components
│   │   │   ├── Landing.tsx
│   │   │   ├── Repository.tsx
│   │   │   ├── Explorer.tsx
│   │   │   └── Architecture.tsx
│   │   ├── store/           # Zustand state management
│   │   │   └── useStore.ts
│   │   ├── lib/             # Utilities
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── backend/
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   ├── github.py
│   │   │   ├── parser.py
│   │   │   ├── graph.py
│   │   │   └── ...
│   │   ├── services/        # Business logic
│   │   │   ├── ast_engine.py
│   │   │   ├── graph_builder.py
│   │   │   ├── dependency_analyzer.py
│   │   │   └── repository_scanner.py
│   │   └── models/          # Data models
│   │       ├── repository.py
│   │       ├── file.py
│   │       └── node.py
│   ├── main.py
│   └── requirements.txt
└── README.md
```

---

## Development

### Backend Development

```bash
cd backend
# Activate virtual environment
pip install -r requirements.txt
python main.py
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Build for Production

```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
# Deploy to Railway/Render or your preferred platform
```

---

## Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
API_HOST=0.0.0.0
API_PORT=8000
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=postgresql://user:password@localhost/codexatlas
CHROMA_DB_PATH=./chroma_db
```

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## Troubleshooting

### Backend Issues

- **Port already in use**: Change `API_PORT` in `.env`
- **Git not found**: Ensure Git is installed and in PATH
- **Import errors**: Ensure all dependencies are installed

### Frontend Issues

- **Port already in use**: Vite will automatically suggest an alternative port
- **API connection errors**: Check that backend is running and `VITE_API_URL` is correct
- **Build errors**: Clear node_modules and reinstall

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

- FastAPI for the amazing Python framework
- React Flow for the graph visualization
- Tree-sitter for AST parsing
- The open-source community

---

## Contact

For questions or support, please open an issue on GitHub.

---

**CodexAtlas AI - Transform Code Into Visual Intelligence**
