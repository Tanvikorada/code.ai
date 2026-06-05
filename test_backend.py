import asyncio
import sys
import os

# add backend path to sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'codexatlas/backend')))

from app.api.github import scan_repository, ScanRequest
from app.api.graph import get_graph
from app.api.architecture import get_architecture
from app.api.health import analyze_health
from app.store import RESULTS_STORE

async def main():
    request = ScanRequest(url="https://github.com/tiangolo/fastapi")
    print(f"Scanning {request.url}...")
    try:
        response = await scan_repository(request)
        repo_id = response.id
        print(f"Scan complete. Repo ID: {repo_id}")
        
        # Test endpoints
        graph = await get_graph(repo_id)
        print(f"Graph Nodes: {len(graph.nodes)}, Edges: {len(graph.edges)}")
        
        arch = await get_architecture(repo_id)
        print(f"Architecture Layers: {len(arch.layers)}")
        for layer in arch.layers:
            print(f"  - {layer['name']}: {len(layer['components'])} components")
            
        health = await analyze_health(repo_id)
        print(f"Health Score: {health.overall_score}")
        for issue in health.issues:
            print(f"  - {issue['severity']}: {issue['message']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
