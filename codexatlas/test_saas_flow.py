import os
import sys
import time
import requests

API_URL = "http://localhost:8000"

def test_flow():
    print("1. Registering new user...")
    username = f"testuser_{int(time.time())}"
    password = "password123"
    email = f"{username}@example.com"
    
    res = requests.post(f"{API_URL}/api/auth/register", json={
        "email": email,
        "password": password
    })
    
    if res.status_code != 200:
        print("Registration failed:", res.text)
        return
    print("Registration successful!")
    
    print("\n2. Logging in...")
    res = requests.post(f"{API_URL}/api/auth/login", data={
        "username": email,
        "password": password
    })
    
    if res.status_code != 200:
        print("Login failed:", res.text)
        return
    token = res.json()["access_token"]
    print("Login successful! Token acquired.")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n3. Initiating Scan...")
    repo_url = "https://github.com/octocat/Hello-World"
    res = requests.post(f"{API_URL}/api/github/scan", json={"url": repo_url}, headers=headers)
    
    if res.status_code != 200:
        print("Scan init failed:", res.text)
        return
        
    repo_id = res.json()["id"]
    print(f"Scan initiated! Repo ID: {repo_id}")
    
    print("\n4. Polling status...")
    status = "processing"
    while status == "processing" or status == "pending":
        time.sleep(2)
        res = requests.get(f"{API_URL}/api/github/status/{repo_id}", headers=headers)
        if res.status_code != 200:
            print("Status fetch failed:", res.text)
            break
        status = res.json()["status"]
        print(f"Current status: {status}")
        
    if status != "completed":
        print("Scan failed or errored out!")
        return
        
    print("\n5. Fetching Graph Data...")
    res = requests.get(f"{API_URL}/api/graph/{repo_id}", headers=headers)
    if res.status_code == 200:
        graph = res.json()
        print(f"Graph Data retrieved! Nodes: {len(graph.get('nodes', []))}, Edges: {len(graph.get('edges', []))}")
    else:
        print("Failed to get graph data:", res.text)
        
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_flow()
