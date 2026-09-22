import sqlite3
import json
import hmac
import hashlib

def export_and_seal_bundle():
    conn = sqlite3.connect("audit.db")
    cursor = conn.cursor()
    
    # Fetch corporate hierarchy
    cursor.execute("SELECT node_id, entity_name, business_number, status, associated_contracts, notes FROM corporate_hierarchy")
    hierarchy = [
        {
            "node_id": row[0],
            "entity_name": row[1],
            "business_number": row[2],
            "status": row[3],
            "associated_contracts": row[4],
            "notes": row[5]
        } for row in cursor.fetchall()
    ]
    
    # Fetch registry cross-checks
    cursor.execute("SELECT entity_number, registry_type, expected_bn, status, verification_note FROM registry_cross_check")
    registries = [
        {
            "entity_number": row[0],
            "registry_type": row[1],
            "expected_bn": row[2],
            "status": row[3],
            "verification_note": row[4]
        } for row in cursor.fetchall()
    ]
    
    # Fetch CRA discrepancy log
    cursor.execute("SELECT entity_id, business_number, portal_status, procurement_binding, discrepancy_analysis FROM cra_discrepancy_log")
    cra_logs = [
        {
            "entity_id": row[0],
            "business_number": row[1],
            "portal_status": row[2],
            "procurement_binding": row[3],
            "discrepancy_analysis": row[4]
        } for row in cursor.fetchall()
    ]
    
    conn.close()
    
    # Build comprehensive bundle payload
    bundle = {
        "framework": "GVT Sovereign Financial Audit Framework",
        "primary_operator": "Jujita Fermin Stairs",
        "primary_entity": "10839477 Canada Inc.",
        "business_number": "749810883RC0001",
        "linked_contracts": ["CW2321555", "CW2123555"],
        "corporate_hierarchy": hierarchy,
        "registry_cross_checks": registries,
        "cra_discrepancy_logs": cra_logs
    }
    
    # Serialize to deterministic JSON string
    bundle_json = json.dumps(bundle, indent=2, sort_keys=True)
    
    # Apply cryptographic HMAC-SHA256 integrity seal
    secret_key = b"GVT_SOVEREIGN_AUDIT_KEY_2026"
    signature = hmac.new(secret_key, bundle_json.encode('utf-8'), hashlib.sha256).hexdigest()
    
    final_package = {
        "data": bundle,
        "hmac_sha256_signature": signature
    }
    
    # Write to file
    output_filename = "gvt_verified_audit_bundle.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_package, f, indent=2)
        
    print(f"[SUCCESS] Exported and sealed updated audit bundle with CRA discrepancy logs.")
    print(f"New Cryptographic Signature: {signature}")

if __name__ == "__main__":
    export_and_seal_bundle()
