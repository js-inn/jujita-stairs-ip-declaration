import sqlite3
import xml.etree.ElementTree as ET
from xml_parser import parse_cra_xml

def init_db(db_path="tax_audit_log.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_ref TEXT UNIQUE,
            transmitter_name TEXT,
            contact_email TEXT,
            payor_name TEXT,
            payor_account_num TEXT,
            total_slips INTEGER,
            total_amount REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            tax_code TEXT,
            payload_hash TEXT
        );

        CREATE TABLE IF NOT EXISTS slips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            recipient_name TEXT,
            recipient_sin TEXT,
            amount REAL,
            FOREIGN KEY (submission_id) REFERENCES submissions(id)
        );

        CREATE TABLE IF NOT EXISTS tax_categories (
            tax_code TEXT PRIMARY KEY,
            tax_description TEXT NOT NULL,
            jurisdiction TEXT NOT NULL,
            authority TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()

def log_submission(model, xml_file_path, ref_num, tax_code, db_path="tax_audit_log.db"):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    t619 = model.t619
    returns = model.returns[0].model_dump() if model.returns else {}
    t4a = returns.get("T4A_OAS", {})
    summary = t4a.get("T4A_OASSummary", {})
    slips = t4a.get("T4A_OASSlip", [])

    cursor.execute("""
        INSERT OR REPLACE INTO submissions (
            submission_ref, transmitter_name, contact_email, payor_name, 
            payor_account_num, total_slips, total_amount, tax_code, payload_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ref_num,
        t619.transmitter_name,
        t619.contact_phone,
        summary.get("bn", "N/A"),
        t619.submitter_acct_num,
        summary.get("total_slips", 0),
        summary.get("total_gross_pay", 0.0),
        tax_code,
        ""
    ))

    cursor.execute("SELECT id FROM submissions WHERE submission_ref = ?", (ref_num,))
    submission_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM slips WHERE submission_id = ?", (submission_id,))

    slip_records = [
        (submission_id, slip.get("recipient_sin", "N/A"), slip.get("sin", "N/A"), slip.get("gross_pay", 0.0))
        for slip in slips
    ]

    cursor.executemany("""
        INSERT INTO slips (submission_id, recipient_name, recipient_sin, amount)
        VALUES (?, ?, ?, ?)
    """, slip_records)

    conn.commit()
    conn.close()
    print(f"Logged submission #{submission_id} (Ref: {ref_num}, Code: {tax_code}) with {len(slips)} slips.")

if __name__ == "__main__":
    xml_path = "cra_submission.xml"
    model = parse_cra_xml(xml_path)
    log_submission(model, xml_file_path=xml_path, ref_num="CRA-T550-2026-001", tax_code="FED_CORP_TAX")
