import sys
import os
import time

# add backend path to sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'codexatlas/backend')))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_full_flow():
    print("=== CodexAtlas End-to-End Flow Test ===")
    
    # 1. Register a test user
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    print(f"\n1. Registering user: {email}...")
    reg_response = client.post("/api/auth/register", json={
        "email": email,
        "password": password
    })
    if reg_response.status_code != 200:
        print(f"Registration failed: {reg_response.text}")
        return
        
    token_data = reg_response.json()
    token = token_data["access_token"]
    print("Registration successful! Token acquired.")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Initiate scan
    repo_url = "https://github.com/octocat/Hello-World"
    print(f"\n2. Initiating scan for {repo_url}...")
    scan_response = client.post("/api/github/scan", json={"url": repo_url}, headers=headers)
    if scan_response.status_code != 200:
        print(f"Scan failed: {scan_response.text}")
        return
        
    repo_id = scan_response.json()["id"]
    scan_msg = scan_response.json()["message"]
    print(f"Scan started. Repo ID: {repo_id} ({scan_msg})")
    
    # 3. Poll status
    status = "processing"
    print("\n3. Polling status...")
    attempts = 0
    while (status == "processing" or status == "pending") and attempts < 15:
        time.sleep(2)
        status_response = client.get(f"/api/github/status/{repo_id}", headers=headers)
        if status_response.status_code != 200:
            print(f"Status call failed: {status_response.text}")
            return
        status = status_response.json()["status"]
        print(f"Current scan status: {status}")
        attempts += 1
        
    if status != "completed":
        print(f"Scan did not complete in time, final status is: {status}")
        return
        
    # 4. Get graph data
    print("\n4. Fetching dependency graph...")
    graph_response = client.get(f"/api/graph/{repo_id}", headers=headers)
    if graph_response.status_code == 200:
        graph_data = graph_response.json()
        print(f"Graph nodes: {len(graph_data.get('nodes', []))}, edges: {len(graph_data.get('edges', []))}")
    else:
        print(f"Graph call failed: {graph_response.text}")
    
    # 5. Get architecture layers
    print("\n5. Fetching architecture layers...")
    arch_response = client.get(f"/api/architecture/{repo_id}", headers=headers)
    if arch_response.status_code == 200:
        arch_data = arch_response.json()
        print(f"Architecture layers found: {len(arch_data.get('layers', []))}")
        for layer in arch_data.get("layers", []):
            print(f"  - {layer.get('name')}: {len(layer.get('components', []))} components")
    else:
        print(f"Architecture call failed: {arch_response.text}")
    
    # 6. Get health metrics
    print("\n6. Fetching health metrics...")
    health_response = client.get(f"/api/health/{repo_id}", headers=headers)
    if health_response.status_code == 200:
        health_data = health_response.json()
        print(f"Health score: {health_data.get('overall_score')}/100")
        print(f"Maintainability: {health_data.get('maintainability')}/100")
        print("Issues found:")
        for issue in health_data.get("issues", []):
            print(f"  - [{issue.get('severity')}] {issue.get('message')}")
    else:
        print(f"Health call failed: {health_response.text}")
    
    # 7. Ask AI question
    print("\n7. Asking AI about the repository...")
    ai_response = client.post("/api/ai/ask", json={
        "repoId": repo_id,
        "question": "What architecture pattern is used in this codebase?"
    }, headers=headers)
    if ai_response.status_code == 200:
        print(f"AI Answer:\n{ai_response.json().get('answer')}")
    else:
        print(f"AI call failed: {ai_response.text}")
    
    # 8. Generate Documentation
    print("\n8. Generating documentation...")
    docs_response = client.post("/api/documentation/generate", json={
        "repoId": repo_id
    }, headers=headers)
    if docs_response.status_code == 200:
        print("Documentation generated successfully!")
        readme = docs_response.json().get('readme', '')
        print(f"Readme snippet:\n{readme[:180].strip()}...")
    else:
        print(f"Documentation call failed: {docs_response.text}")

if __name__ == "__main__":
    test_full_flow()

