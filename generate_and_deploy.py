import json
import hashlib
import datetime
import os

LEDGER_FILE = "wire_ledger.json"
MANIFEST_FILE = "MANIFEST.json"

def calculate_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest():
    ledger_hash = calculate_sha256(LEDGER_FILE)
    
    manifest_data = {
        "entity": "10839477 Canada Inc.",
        "jurisdiction": "Canada (Federal)",
        "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a",
        "cryptographic_anchor_uuid": "3d9f8a21-c5e7-4b6a-9128-f0d3e2a1b9c7",
        "last_updated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "related_contracts": ["CW2321555", "CW2123555"],
        "ledger_proof": {
            "file": LEDGER_FILE,
            "hash_algorithm": "SHA-256",
            "sha256": ledger_hash
        }
    }

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest_data, f, indent=4)

    print(f"Successfully updated {MANIFEST_FILE} with SHA-256 proof: {ledger_hash}")

if __name__ == "__main__":
    generate_manifest()
