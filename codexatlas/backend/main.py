# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import engine, Base
from app.api import github, graph, architecture, documentation, health, ai, auth

# Create database tables (now managed by Alembic)
# Base.metadata.create_all(bind=engine)

# Initialize slowapi rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="CodexAtlas API",
    description="Visual Intelligence Layer For Software Systems",
    version="1.0.0"
)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

import os

# Get frontend URL from environment (default to localhost for dev)
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    FRONTEND_URL,
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.onrender\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(github.router, prefix="/api/github", tags=["github"])

app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(architecture.router, prefix="/api/architecture", tags=["architecture"])
app.include_router(documentation.router, prefix="/api/documentation", tags=["documentation"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    return {
        "message": "CodexAtlas API",
        "version": "1.0.0",
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
