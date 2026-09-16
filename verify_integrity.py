import sqlite3
import hashlib
import os
import sys

DB_FILE = "tax_audit_log.db"
XML_FILE = "cra_submission.xml"
SUBMISSION_REF = "CRA-T550-2026-001"

def calculate_sha256(file_path: str) -> str:
    """Compute the SHA-256 digest of a target file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_payload_integrity(ref_num: str, file_path: str):
    if not os.path.exists(file_path):
        print(f"❌ ERROR: XML file '{file_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(DB_FILE):
        print(f"❌ ERROR: Database '{DB_FILE}' does not exist.")
        sys.exit(1)

    # 1. Compute current hash from disk
    current_hash = calculate_sha256(file_path)

    # 2. Fetch stored hash from SQLite
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT payload_hash, tax_code FROM submissions WHERE submission_ref = ?", 
            (ref_num,)
        )
        row = cursor.fetchone()

    if not row:
        print(f"❌ ERROR: Submission reference '{ref_num}' not found in database.")
        sys.exit(1)

    stored_hash, tax_code = row

    if not stored_hash:
        print(f"⚠️ WARNING: No stored hash found in database for submission '{ref_num}'.")
        sys.exit(1)

    # 3. Perform Integrity Check
    print("=" * 80)
    print(" 🔒 PAYLOAD INTEGRITY AUDIT VERIFICATION")
    print("=" * 80)
    print(f" Submission Ref : {ref_num}")
    print(f" Tax Category   : {tax_code}")
    print(f" Target File    : {file_path}")
    print(f" Stored Hash    : {stored_hash}")
    print(f" Disk Hash      : {current_hash}")
    print("-" * 80)

    if current_hash == stored_hash:
        print(" SUCCESS: Payload integrity verified. File has NOT been modified.")
        print("=" * 80)
    else:
        print(" 🚨 ALERT: TAMPERING DETECTED! File hash does NOT match the audit log.")
        print("=" * 80)
        sys.exit(1)

if __name__ == "__main__":
    verify_payload_integrity(SUBMISSION_REF, XML_FILE)
