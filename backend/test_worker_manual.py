import sys
import os
import uuid

os.chdir(r"c:\Users\Tanvi\Desktop\code.AI\backend")
sys.path.append(os.getcwd())

from app.services.worker import process_repository
from app.models.orm import ScanResult, User
from app.database import SessionLocal, engine
from app.models.orm import Base

Base.metadata.create_all(bind=engine)

db = SessionLocal()
user = db.query(User).filter_by(username="test_worker_user").first()
if not user:
    user = User(username="test_worker_user", email="test@worker.com", hashed_password="pw")
    db.add(user)
    db.commit()

repo_id = str(uuid.uuid4())
scan = ScanResult(id=repo_id, user_id=user.id, repo_url="https://github.com/Tanvikorada/code.ai", status="processing")
db.add(scan)
db.commit()

print(f"Starting process_repository for {repo_id}...")
try:
    process_repository(repo_id, "https://github.com/Tanvikorada/code.ai")
except Exception as e:
    print("Exception caught:", e)

db.refresh(scan)
print(f"Status: {scan.status}")
if scan.status == "failed":
    print("Error data:", scan.data)
else:
    print("Success. Nodes count:", len(scan.data.get("graph", {}).get("nodes", [])))
