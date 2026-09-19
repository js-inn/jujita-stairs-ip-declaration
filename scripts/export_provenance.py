import sqlite3
import json
import hashlib
import uuid
from datetime import datetime, UTC

DB_PATH = "local_audit.db"
EXPORT_PATH = "manifests/portfolio-provenance-manifest.json"

def export_provenance():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fetch all parsed records
    cursor.execute('''
        SELECT source_institution, ip_id, asset_title, asset_class, 
               valuation, compliance_standard, status, ingested_at 
        FROM parsed_records
    ''')
    rows = cursor.fetchall()
    
    assets = []
    total_valuation = 0.0
    
    for row in rows:
        asset = {
            "source_institution": row[0],
            "ip_id": row[1],
            "asset_title": row[2],
            "asset_class": row[3],
            "valuation": row[4],
            "compliance_standard": row[5],
            "status": row[6],
            "ingested_at": row[7]
        }
        assets.append(asset)
        total_valuation += row[4] if row[4] else 0.0

    conn.close()

    # Generate cryptographic provenance anchor
    export_payload = {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "name": "Decentralized IP Declaration and Asset Registry",
        "creator": "10839477 Canada Inc.",
        "publisher": "Jujita Fermin Stairs",
        "jurisdiction": "Edmonton, Alberta, Canada",
        "provenanceAnchorId": f"urn:uuid:{str(uuid.uuid4())}",
        "timestamp": datetime.now(UTC).isoformat(),
        "totalAssets": len(assets),
        "totalValuation": total_valuation,
        "assets": assets
    }

    # Serialize and compute SHA-256 cryptographic provenance hash
    payload_str = json.dumps(export_payload, sort_keys=True, indent=2)
    provenance_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

    # Wrap with cryptographic verification envelope
    final_manifest = {
        "provenanceHash": provenance_hash,
        "algorithm": "SHA-256",
        "manifest": export_payload
    }

    # Save to file
    with open(EXPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(final_manifest, f, indent=2)

    print("=" * 60)
    print("      CRYPTOGRAPHIC PROVENANCE EXPORT SUCCESSFUL")
    print("=" * 60)
    print(f"Export Target    : {EXPORT_PATH}")
    print(f"Cryptographic ID : {export_payload['provenanceAnchorId']}")
    print(f"SHA-256 Hash     : {provenance_hash}")
    print(f"Total Assets     : {len(assets)}")
    print(f"Total Valuation  : ${total_valuation:,.2f}")
    print("=" * 60)

if __name__ == "__main__":
    export_provenance()
