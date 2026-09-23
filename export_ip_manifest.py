import sqlite3
import json
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"
MANIFEST_FILE = "ip_disclosure_manifest.json"

def export_manifest():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    manifest_data = {
        "manifest_metadata": {
            "title": "Sovereign Institutional and Intellectual Property Audit Manifest",
            "issuer": "10839477 Canada Inc.",
            "author": "Jujita Fermin Stairs",
            "jurisdiction": "Edmonton, Alberta, Canada",
            "timestamp": datetime.now().isoformat(),
            "schema_version": "1.0.0"
        },
        "hierarchies": [],
        "academic_citations": [],
        "gateways": []
    }
    
    # 1. Fetch Corporate & Governmental Hierarchies
    try:
        cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction, timestamp, hierarchy_anchor FROM corporate_hierarchy")
        rows = cursor.fetchall()
        for parent, child, rel, juris, ts, anchor in rows:
            manifest_data["hierarchies"].append({
                "parent_entity": parent,
                "child_entity": child,
                "relationship_type": rel,
                "jurisdiction": juris,
                "timestamp": ts,
                "hierarchy_anchor": anchor
            })
    except sqlite3.OperationalError:
        pass

    # 2. Fetch Academic Citations
    try:
        cursor.execute("SELECT research_paper_title, author_institution, referenced_module, doi_identifier, timestamp, citation_anchor FROM academic_citations")
        rows = cursor.fetchall()
        for title, inst, mod, doi, ts, anchor in rows:
            manifest_data["academic_citations"].append({
                "research_paper_title": title,
                "author_institution": inst,
                "referenced_module": mod,
                "doi_identifier": doi,
                "timestamp": ts,
                "citation_anchor": anchor
            })
    except sqlite3.OperationalError:
        pass

    # 3. Fetch Gateway Nodes (if present)
    try:
        cursor.execute("SELECT name, institution_type, clearing_system, jurisdiction FROM gateway_nodes")
        rows = cursor.fetchall()
        for name, itype, clearing, juris in rows:
            manifest_data["gateways"].append({
                "name": name,
                "institution_type": itype,
                "clearing_system": clearing,
                "jurisdiction": juris
            })
    except sqlite3.OperationalError:
        pass

    conn.close()
    
    # Generate cryptographic signature for the complete manifest payload
    manifest_json_string = json.dumps(manifest_data, sort_keys=True)
    manifest_signature = hmac.new(SECRET_KEY, manifest_json_string.encode('utf-8'), hashlib.sha256).hexdigest()
    
    final_output = {
        "payload": manifest_data,
        "cryptographic_proof": {
            "algorithm": "HMAC-SHA256",
            "root_signature": manifest_signature
        }
    }
    
    # Write to file
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4)
        
    print(f"\n=======================================================================")
    print(f"[*] IP DISCLOSURE MANIFEST EXPORTED SUCCESSFULLY")
    print(f"    File Name: {MANIFEST_FILE}")
    print(f"    Total Hierarchies: {len(manifest_data['hierarchies'])}")
    print(f"    Total Citations: {len(manifest_data['academic_citations'])}")
    print(f"    Root HMAC Signature: {manifest_signature}")
    print(f"=======================================================================\n")

if __name__ == "__main__":
    export_manifest()
