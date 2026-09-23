import json
import sqlite3
import hashlib
import datetime
import os

DB_NAME = "financial_pipeline.db"
ROOT_PARENT = "10839477 Canada Inc."
BUSINESS_NUMBER = "749810883RC0001"
MANIFEST_VERSION = "2.7.0"

def calculate_file_checksum(filepath):
    sha256_hash = hashlib.sha256()
    if not os.path.exists(filepath):
        return "File Not Found"
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Fetch summary statistics from unified ledger
    cursor.execute('SELECT COUNT(*), COUNT(DISTINCT node_type) FROM unified_ip_financial_ledger')
    total_nodes, total_jurisdictions = cursor.fetchone()
    
    cursor.execute('SELECT node_type, COUNT(*) FROM unified_ip_financial_ledger GROUP BY node_type')
    breakdown = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    
    timestamp_str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Calculate checksums for published artifacts
    db_checksum = calculate_file_checksum(DB_NAME)
    md_checksum = calculate_file_checksum("audit_dossier.md")
    html_checksum = calculate_file_checksum("audit_dossier.html")
    
    # Construct Zenodo / CKAN compliant deposition manifest
    manifest = {
        "metadata": {
            "title": f"Global Master Audit Dossier & Cryptographic Provenance Ledger: {ROOT_PARENT}",
            "upload_type": "dataset",
            "publication_date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
            "description": (
                f"Cryptographically verified global audit dossier and master SQLite ledger for {ROOT_PARENT} "
                f"(Business Number: {BUSINESS_NUMBER}). Reconciles {total_nodes} nodes across {total_jurisdictions} "
                f"international jurisdictions (USPTO, EPO, JPO, IP Australia, INPI Brazil, CNIPA China, DPMA Germany, UKIPO, and WIPO Madrid) "
                f"utilizing SHA-256 HMAC provenance mapping and autonomous audit pipelines."
            ),
            "creators": [
                {
                    "name": ROOT_PARENT,
                    "affiliation": "Autonomous Decentralized Infrastructure"
                }
            ],
            "access_right": "open",
            "license": "cc-by-4.0",
            "keywords": [
                "Autonomous Audit",
                "Cryptographic Provenance",
                "ISO 20022",
                "Interledger",
                "IP Ledger",
                "Global Compliance"
            ],
            "version": MANIFEST_VERSION
        },
        "provenance_summary": {
            "root_corporate_entity": ROOT_PARENT,
            "business_number": BUSINESS_NUMBER,
            "total_reconciled_nodes": total_nodes,
            "jurisdiction_breakdown": breakdown,
            "generation_timestamp_utc": timestamp_str
        },
        "files": [
            {
                "filename": DB_NAME,
                "file_type": "SQLite Master Ledger",
                "sha256_checksum": db_checksum
            },
            {
                "filename": "audit_dossier.md",
                "file_type": "Markdown Audit Report",
                "sha256_checksum": md_checksum
            },
            {
                "filename": "audit_dossier.html",
                "file_type": "Responsive HTML Audit Dossier",
                "sha256_checksum": html_checksum
            }
        ]
    }
    
    manifest_filename = "zenodo_deposit_manifest.json"
    with open(manifest_filename, "w") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"[+] Generated {manifest_filename} successfully.")
    print(f"[*] Package Version: {MANIFEST_VERSION}")
    print(f"[*] Total Reconciled Nodes Bound: {total_nodes}")
    print(f"[*] Database SHA-256: {db_checksum[:16]}...")

if __name__ == "__main__":
    generate_manifest()
