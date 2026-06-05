from typing import Dict, Any

# In-memory store for repository scan results
# Format:
# {
#     "repo_id": {
#         "graph": {"nodes": [...], "edges": [...]},
#         "architecture": {"layers": [...], "metrics": {...}},
#         "health": {"overall_score": 0, "issues": [...], ...},
#         "metadata": {"name": "", "url": "", "framework": "", "language": ""}
#     }
# }
RESULTS_STORE: Dict[str, Dict[str, Any]] = {}
