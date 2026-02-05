import shutil
import sys
import firebase_admin
from firebase_admin import credentials, firestore

DATASET_NAME = "sample_csv"
ROLLBACK_VERSION = sys.argv[1]

WORKING_FILE = "data/dataset.csv"

# ---------- Firebase init ----------
cred = credentials.Certificate("secret/firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------- Get version metadata ----------
doc = (
    db.collection("datasets")
      .document(DATASET_NAME)
      .collection("versions")
      .document(ROLLBACK_VERSION)
      .get()
)

if not doc.exists:
    print("❌ Version not found")
    sys.exit(1)

version_path = doc.to_dict()["file_path"]

# ---------- Rollback ----------
shutil.copyfile(version_path, WORKING_FILE)

print(f"⏪ Rolled back to {ROLLBACK_VERSION}")
