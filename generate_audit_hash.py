import hashlib
import json

def generate_audit_payload_hash(manifest_path="published_audit_manifest.json"):
    """
    Reads the verified audit manifest and generates a deterministic 
    cryptographic hash to be anchored.
    """
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)
    
    # Canonicalize JSON payload to ensure exact byte consistency
    canonical_payload = json.dumps(manifest_data, sort_keys=True, separators=(',', ':'))
    
    # Generate SHA-256 cryptographic anchor
    payload_hash = hashlib.sha256(canonical_payload.encode('utf-8')).hexdigest()
    
    print(f"Cryptographic Anchor Hash Generated: {payload_hash}")
    return payload_hash.encode('utf-8')

if __name__ == "__main__":
    sig_payload = generate_audit_payload_hash()
