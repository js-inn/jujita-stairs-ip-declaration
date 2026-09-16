import sqlite3
import hashlib
import os

DB_FILE = "tax_audit_log.db"
XML_FILE = "cra_submission.xml"
SUBMISSION_REF = "CRA-T550-2026-001"

def calculate_sha256(file_path: str) -> str:
    """Compute the SHA-256 digest of a target file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in 64kb chunks for memory efficiency
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def log_hash_to_db(ref_num: str, file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: Target XML file '{file_path}' not found.")
        return

    # Compute hash
    payload_hash = calculate_sha256(file_path)
    print(f"Calculated SHA-256 Hash: {payload_hash}")

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # 1. Ensure 'payload_hash' column exists in 'submissions'
        cursor.execute("PRAGMA table_info(submissions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "payload_hash" not in columns:
            cursor.execute("ALTER TABLE submissions ADD COLUMN payload_hash TEXT")
            print("Added 'payload_hash' column to 'submissions' table.")

        # 2. Update the target record with the payload hash
        cursor.execute("""
            UPDATE submissions 
            SET payload_hash = ? 
            WHERE submission_ref = ?
        """, (payload_hash, ref_num))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Successfully logged SHA-256 hash for submission '{ref_num}'.")
        else:
            print(f"Warning: Submission reference '{ref_num}' not found in database.")

if __name__ == "__main__":
    log_hash_to_db(SUBMISSION_REF, XML_FILE)
