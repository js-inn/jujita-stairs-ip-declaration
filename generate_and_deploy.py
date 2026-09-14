import json
import datetime
import subprocess

MANIFEST_FILE = "MANIFEST.json"

def update_manifest():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    manifest_data = {
        "entity": "10839477 Canada Inc.",
        "creator": "Jujita Fermin Stairs",
        "creator_uuid": "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a",
        "crypto_anchor": "3d9f8a21-c5e7-4b6a-9128-f0d3e2a1b9c7",
        "last_updated": timestamp,
        "government_contracts": [
            "CW2321555",
            "CW2123555"
        ]
    }

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest_data, f, indent=4)

    print(f"Successfully generated {MANIFEST_FILE} with contract references!")

if __name__ == "__main__":
    update_manifest()
