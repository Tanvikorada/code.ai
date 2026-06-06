import os
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import subprocess
import tempfile
import shutil

class RepositoryScanner:
    """Scan and analyze repositories"""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
    
    def clone_repository(self, url: str) -> str:
        """Clone a repository to a temporary directory"""
        import uuid
        repo_name = url.split('/')[-1].replace('.git', '')
        # Add a UUID to prevent folder concurrency crashes
        clone_path = os.path.join(self.temp_dir, f"codexatlas_{repo_name}_{uuid.uuid4().hex[:8]}")
        
        # Remove if exists (rare now due to UUID, but good practice)
        def remove_readonly(func, path, excinfo):
            import stat
            os.chmod(path, stat.S_IWRITE)
            func(path)
            
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, onerror=remove_readonly)
        
        try:
            # Check repo size first via git ls-remote or GitHub API (simplified here by using depth 1 and strict timeout)
            # Use --depth 1 to prevent downloading huge git histories, and a 30-second timeout
            subprocess.run(
                ['git', 'clone', '--depth', '1', '--single-branch', url, clone_path],
                check=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check directory size after cloning to prevent processing massive repos
            total_size = 0
            for dirpath, _, filenames in os.walk(clone_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            
            # Limit to configured max size (default 200MB)
            max_mb = int(os.environ.get("MAX_REPO_SIZE_MB", 200))
            if total_size > max_mb * 1024 * 1024:
                self.cleanup(clone_path)
                raise Exception(f"Repository exceeds the maximum allowed size of {max_mb}MB.")
                
            return clone_path
        except subprocess.TimeoutExpired as e:
            self.cleanup(clone_path)
            raise Exception("Repository clone timed out. It might be too large or network is slow.")
        except subprocess.CalledProcessError as e:
            self.cleanup(clone_path)
            raise Exception(f"Failed to clone repository: {e.stderr}")
    
    def detect_language(self, repo_path: str) -> str:
        """Detect the primary language of the repository"""
        language_counts = {
            'python': 0,
            'javascript': 0,
            'typescript': 0,
            'go': 0,
            'rust': 0,
            'java': 0,
        }
        
        extensions = {
            'python': ['.py'],
            'javascript': ['.js', '.jsx'],
            'typescript': ['.ts', '.tsx'],
            'go': ['.go'],
            'rust': ['.rs'],
            'java': ['.java'],
        }
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common non-code directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
            
            for file in files:
                for lang, exts in extensions.items():
                    if any(file.endswith(ext) for ext in exts):
                        language_counts[lang] += 1
        
        # Return the language with the most files
        dominant_lang = max(language_counts, key=language_counts.get)
        return dominant_lang if language_counts[dominant_lang] > 0 else 'unknown'
    
    def detect_framework(self, repo_path: str, language: str) -> str:
        """Detect the framework being used"""
        framework = 'unknown'
        
        # Check for package.json (JavaScript/TypeScript)
        if os.path.exists(os.path.join(repo_path, 'package.json')):
            with open(os.path.join(repo_path, 'package.json'), 'r') as f:
                package_json = f.read()
                if 'react' in package_json:
                    framework = 'React'
                elif 'vue' in package_json:
                    framework = 'Vue'
                elif 'angular' in package_json:
                    framework = 'Angular'
                elif 'next' in package_json:
                    framework = 'Next.js'
                elif 'express' in package_json:
                    framework = 'Express'
        
        # Check for requirements.txt (Python)
        if os.path.exists(os.path.join(repo_path, 'requirements.txt')):
            with open(os.path.join(repo_path, 'requirements.txt'), 'r') as f:
                requirements = f.read()
                if 'django' in requirements:
                    framework = 'Django'
                elif 'flask' in requirements:
                    framework = 'Flask'
                elif 'fastapi' in requirements:
                    framework = 'FastAPI'
        
        # Check for go.mod (Go)
        if os.path.exists(os.path.join(repo_path, 'go.mod')):
            framework = 'Go Module'
        
        # Check for Cargo.toml (Rust)
        if os.path.exists(os.path.join(repo_path, 'Cargo.toml')):
            framework = 'Cargo'
        
        return framework
    
    def get_file_structure(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get the file structure of the repository"""
        files = []
        
        for root, dirs, filenames in os.walk(repo_path):
            # Skip hidden directories and common non-code directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env', 'dist', 'build', '.git']]
            
            for filename in filenames:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, repo_path)
                
                # Get file extension
                _, ext = os.path.splitext(filename)
                
                # Determine language
                language = self._get_language_from_ext(ext)
                
                file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
                
                # Skip files larger than 1MB to prevent memory exhaustion during parsing
                if file_size > 1024 * 1024:
                    continue
                
                files.append({
                    'path': relative_path,
                    'absolute_path': file_path,
                    'extension': ext,
                    'language': language,
                    'size': file_size
                })
        
        return files
    
    def _get_language_from_ext(self, ext: str) -> str:
        """Map file extension to language"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.go': 'go',
            '.rs': 'rust',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.css': 'css',
            '.scss': 'scss',
            '.html': 'html',
            '.json': 'json',
            '.md': 'markdown',
            '.yaml': 'yaml',
            '.yml': 'yaml',
        }
        return ext_map.get(ext.lower(), 'unknown')
    
    def cleanup(self, repo_path: str):
        """Remove temporary repository clone"""
        def remove_readonly(func, path, excinfo):
            import stat
            os.chmod(path, stat.S_IWRITE)
            func(path)
            
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path, onerror=remove_readonly)
