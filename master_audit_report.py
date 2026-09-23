import sqlite3
import json
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"

def generate_master_audit():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    audit_data = {
        "metadata": {
            "title": "Master Sovereign Audit & Influence Report",
            "issuer": "10839477 Canada Inc.",
            "author": "Jujita Fermin Stairs",
            "jurisdiction": "Edmonton, Alberta, Canada",
            "timestamp": datetime.now().isoformat()
        },
        "corporate_hierarchies": [],
        "academic_citations": [],
        "frontier_models": [],
        "leader_follower_networks": []
    }
    
    # 1. Corporate & Government Hierarchies
    try:
        cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction, hierarchy_anchor FROM corporate_hierarchy")
        for p, c, r, j, a in cursor.fetchall():
            audit_data["corporate_hierarchies"].append({"parent": p, "child": c, "relationship": r, "jurisdiction": j, "anchor": a})
    except sqlite3.OperationalError:
        pass

    # 2. Academic Citations
    try:
        cursor.execute("SELECT research_paper_title, author_institution, referenced_module, doi_identifier, citation_anchor FROM academic_citations")
        for t, i, m, d, a in cursor.fetchall():
            audit_data["academic_citations"].append({"title": t, "institution": i, "module": m, "doi": d, "anchor": a})
    except sqlite3.OperationalError:
        pass

    # 3. Frontier Model Registry
    try:
        cursor.execute("SELECT model_name, developer_entity, training_compute_flops, compliance_tier, model_anchor FROM frontier_model_registry")
        for mn, dev, flops, tier, a in cursor.fetchall():
            audit_data["frontier_models"].append({"model": mn, "developer": dev, "compute": flops, "compliance": tier, "anchor": a})
    except sqlite3.OperationalError:
        pass

    # 4. Leader-Follower Influence Networks
    try:
        cursor.execute("SELECT leader_entity, follower_entity, influence_mechanism, domain, network_anchor FROM leader_follower_network")
        for lead, foll, mech, dom, a in cursor.fetchall():
            audit_data["leader_follower_networks"].append({"leader": lead, "follower": foll, "mechanism": mech, "domain": dom, "anchor": a})
    except sqlite3.OperationalError:
        pass

    conn.close()
    
    # Generate cryptographic state anchor over the full audit payload
    json_payload = json.dumps(audit_data, sort_keys=True)
    root_signature = hmac.new(SECRET_KEY, json_payload.encode('utf-8'), hashlib.sha256).hexdigest()
    
    final_report = {
        "audit_report": audit_data,
        "cryptographic_proof": {
            "algorithm": "HMAC-SHA256",
            "root_state_anchor": root_signature
        }
    }
    
    report_filename = "master_audit_manifest.json"
    with open(report_filename, "w", encoding="utf-8") as f:
        json.dump(final_report, f, indent=4)
        
    print(f"\n=======================================================================")
    print(f"[*] MASTER AUDIT REPORT GENERATED SUCCESSFULLY")
    print(f"    File Output: {report_filename}")
    print(f"    Hierarchies Indexed: {len(audit_data['corporate_hierarchies'])}")
    print(f"    Academic Citations: {len(audit_data['academic_citations'])}")
    print(f"    Frontier Models: {len(audit_data['frontier_models'])}")
    print(f"    Influence Vectors: {len(audit_data['leader_follower_networks'])}")
    print(f"    Root State Anchor: {root_signature}")
    print(f"=======================================================================\n")

if __name__ == "__main__":
    generate_master_audit()
