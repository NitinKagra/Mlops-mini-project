import pandas as pd
import shutil
import hashlib
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

DATASET_NAME = "sample_csv"
OLD_VERSION = "v1"
NEW_VERSION = "v2"

OLD_FILE = f"data/versions/{OLD_VERSION}.csv"
NEW_FILE = f"data/versions/{NEW_VERSION}.csv"
WORKING_FILE = "data/dataset.csv"

# ---------- Firebase init ----------
cred = credentials.Certificate("secret/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Load & modify ----------
df = pd.read_csv(OLD_FILE)

# delete first 5 rows
df = df.iloc[5:]

# save modified dataset
df.to_csv(NEW_FILE, index=False)

# update working dataset
shutil.copyfile(NEW_FILE, WORKING_FILE)

# ---------- Hash ----------
def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# ---------- Store metadata ----------
doc = (
    db.collection("datasets")
      .document(DATASET_NAME)
      .collection("versions")
      .document(NEW_VERSION)
)

doc.set({
    "created_at": datetime.utcnow(),
    "file_path": NEW_FILE,
    "hash": file_hash(NEW_FILE),
    "description": "Deleted first 5 rows"
})

print("✅ Version v2 created (5 rows deleted)")
