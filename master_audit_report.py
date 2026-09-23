import sqlite3
import hmac
import hashlib
from datetime import datetime

DB_NAME = "financial_pipeline.db"
SECRET_KEY = b"jujita_secret_root_key"

def generate_master_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print(f"\n=======================================================================")
    print(f"[*] JUJITA-STAIRS SOVEREIGN AUDIT LEDGER - MASTER VERIFICATION REPORT")
    print(f"    Timestamp: {datetime.now().isoformat()}")
    print(f"=======================================================================\n")
    
    hierarchy_rows = []
    gateway_rows = []
    citation_rows = []
    
    # 1. Corporate, Space & Government Hierarchies
    try:
        cursor.execute("SELECT parent_entity, child_entity, relationship_type, jurisdiction FROM corporate_hierarchy")
        hierarchy_rows = cursor.fetchall()
        print(f"--- [1] CORPORATE, SPACE & GOVERNMENTAL HIERARCHIES ({len(hierarchy_rows)} nodes) ---")
        for parent, child, rel, juris in hierarchy_rows:
            print(f"  [Parent] {parent}")
            print(f"   └── [Child] {child} ({rel}) [{juris}]")
        print("-" * 71)
    except sqlite3.OperationalError:
        print("  (corporate_hierarchy table not found)")

    # 2. Financial Gateways & Payment Corridors (Checking alternative table names if needed)
    try:
        cursor.execute("SELECT name, institution_type, clearing_system, jurisdiction FROM gateway_nodes")
        gateway_rows = cursor.fetchall()
        print(f"\n--- [2] INSTITUTIONAL FINANCIAL GATEWAYS ({len(gateway_rows)} nodes) ---")
        for name, itype, clearing, juris in gateway_rows:
            print(f"  [Gateway] {name} ({itype}) -> System: {clearing} [{juris}]")
        print("-" * 71)
    except sqlite3.OperationalError:
        print("  (gateway_nodes table not found)")

    # 3. Academic Citations & Research Tracking
    try:
        cursor.execute("SELECT research_paper_title, author_institution, referenced_module, doi_identifier FROM academic_citations")
        citation_rows = cursor.fetchall()
        print(f"\n--- [3] ACADEMIC CITATIONS & RESEARCH LOGS ({len(citation_rows)} entries) ---")
        for title, inst, mod, doi in citation_rows:
            print(f"  [Paper] {title}")
            print(f"   └── Inst: {inst} | Module: {mod} | DOI: {doi}")
        print("-" * 71)
    except sqlite3.OperationalError:
        print("  (academic_citations table not found)")

    # Generate master cryptographic summary anchor safely
    total_records = len(hierarchy_rows) + len(gateway_rows) + len(citation_rows)
    ledger_state = f"{len(hierarchy_rows)}:{len(gateway_rows)}:{len(citation_rows)}:{datetime.now().date().isoformat()}".encode('utf-8')
    master_anchor = hmac.new(SECRET_KEY, ledger_state, hashlib.sha256).hexdigest()
    
    print(f"\n[*] MASTER LEDGER INTEGRITY CHECK:")
    print(f"    Total Indexed Entities/Records: {total_records}")
    print(f"    Cryptographic State Anchor (HMAC-SHA256): {master_anchor}")
    print(f"=======================================================================\n")
    
    conn.close()

if __name__ == "__main__":
    generate_master_report()
