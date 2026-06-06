# CodexAtlas AI - Quick Start Guide

## 🚀 Quick Start (Windows PowerShell)

### Backend Setup

```powershell
# Navigate to backend
cd codexatlas\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python main.py
```

Backend will run on: `http://localhost:8000`

### Frontend Setup

```powershell
# Open a new PowerShell terminal
cd codexatlas\frontend

# Install dependencies
npm install

# Run the frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

---

## 📦 Prerequisites

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads))

---

## 🎯 Usage

1. Open `http://localhost:5173` in your browser
2. Paste a GitHub repository URL (e.g., `https://github.com/facebook/react`)
3. Click "Scan Repository"
4. Explore the visual dependency graph
5. Switch to Architecture View to see system layers

---

## 🔧 Troubleshooting

### Port already in use
```powershell
# Kill process on port 8000 (backend)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Kill process on port 5173 (frontend)
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

### Python virtual environment issues
```powershell
# Delete and recreate venv
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Node modules issues
```powershell
# Delete node_modules and package-lock.json
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## 📝 Environment Variables

### Backend (`codexatlas/backend/.env`)
```env
API_HOST=0.0.0.0
API_PORT=8000
GROQ_API_KEY=your_key_here
```

### Frontend (`codexatlas/frontend/.env`)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🏗️ Project Structure

```
codexatlas/
├── frontend/          # React + TypeScript frontend
│   ├── src/
│   │   ├── pages/     # Landing, Repository, Explorer, Architecture
│   │   ├── store/     # Zustand state management
│   │   └── lib/       # API client
├── backend/           # FastAPI + Python backend
│   ├── app/
│   │   ├── api/       # API endpoints (github, parser, graph, etc.)
│   │   ├── services/  # AST engine, graph builder, dependency analyzer
│   │   └── models/    # Data models
└── README.md          # Full documentation
```

---

## 🎨 Features

- ✅ Visual dependency graph with React Flow
- ✅ AST-based code parsing
- ✅ Knowledge graph generation
- ✅ Architecture layer detection
- ✅ Health analysis
- ✅ AI-powered questions
- ✅ Auto documentation
- ✅ Impact analysis

---

## 🚀 Next Steps

1. Run both frontend and backend
2. Scan a repository
3. Explore the visual graph
4. Check architecture view
5. Try AI chat feature

**Happy Coding! 🎉**
