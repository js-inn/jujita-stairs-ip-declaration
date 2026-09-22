import sqlite3
import os

def find_db():
    # Search common directories for the audit database
    search_paths = [
        "investments_audit.db",
        os.path.expanduser("~/investments_audit.db"),
        os.path.expanduser("~/downloads/investments_audit.db"),
        "/storage/emulated/0/Government_Contracts_Compliance/compliance_pipeline.db"
    ]
    for path in search_paths:
        if os.path.exists(path):
            return path
    return None

def view_portfolio_amounts():
    db_path = find_db()
    if not db_path:
        print("[ERROR] Could not locate 'investments_audit.db' anywhere on the device.")
        return

    print(f"[FOUND] Using database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check which tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Available tables: {tables}")

    if "investments" in tables:
        cursor.execute("SELECT account_type, institution, security_name, identifier, value_cad FROM investments")
        rows = cursor.fetchall()
        print("\n==========================================")
        print(" DETAILED INVESTMENT & TRUST AUDIT AMOUNTS")
        print("==========================================")
        grand_total = 0.0
        for idx, row in enumerate(rows, 1):
            acc_type, institution, security, ident, val = row
            val_formatted = f"${val:,.2f} CAD" if val else "$0.00 CAD"
            grand_total += (val or 0.0)
            print(f"[{idx}] {acc_type} | {institution}")
            print(f"    • Security/Asset: {security or 'N/A'} (ID: {ident or 'N/A'})")
            print(f"    • Value: {val_formatted}\n")
        print("-" * 42)
        print(f" GRAND TOTAL PORTFOLIO VALUE: ${grand_total:,.2f} CAD")
        print("==========================================")
    elif "trust_reconciliation" in tables:
        cursor.execute("SELECT * FROM trust_reconciliation")
        rows = cursor.fetchall()
        print("\n==========================================")
        print(" TRUST RECONCILIATION RECORDS")
        print("==========================================")
        for idx, row in enumerate(rows, 1):
            print(f"[{idx}] {row}")
        print("==========================================")
    else:
        print("No matching investment or trust tables found in this database.")

    conn.close()

if __name__ == '__main__':
    view_portfolio_amounts()




