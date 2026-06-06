FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies (e.g. for git, tree-sitter, etc)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create a data directory for the SQLite database
RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/codexatlas.db

# Copy project
COPY . .

# Run migrations and then start the application
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT
