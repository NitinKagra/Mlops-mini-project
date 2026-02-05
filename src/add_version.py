import shutil
import hashlib
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

DATASET_NAME = "sample_csv"
VERSION = "v1"
SOURCE_FILE = "data/dataset.csv"
VERSION_FILE = f"data/versions/{VERSION}.csv"

# ---------- Firebase init ----------
cred = credentials.Certificate("secret/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Copy dataset ----------
shutil.copyfile(SOURCE_FILE, VERSION_FILE)

# ---------- Compute hash ----------
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# ---------- Store metadata ----------
doc = (
    db.collection("datasets")
      .document(DATASET_NAME)
      .collection("versions")
      .document(VERSION)
)

doc.set({
    "created_at": datetime.utcnow(),
    "file_path": VERSION_FILE,
    "hash": file_hash(VERSION_FILE),
    "description": "Initial dataset version"
})

print("✅ Version v1 registered")
