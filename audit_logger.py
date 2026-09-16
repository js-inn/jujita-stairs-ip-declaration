import sqlite3
import hashlib
import os
from xml_deserializer import cra_xml_to_pydantic

DB_FILE = "tax_audit_log.db"

def calculate_sha256(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def log_submission(submission_model, xml_file_path: str, ref_num: str = "SUB-001", tax_code: str = "FED_CORP_TAX"):
    t619 = submission_model.T619
    summary = submission_model.T550.Summary
    slips = submission_model.T550.Slips
    
    payload_hash = calculate_sha256(xml_file_path) if os.path.exists(xml_file_path) else None
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO submissions (
                submission_ref, transmitter_name, contact_email, 
                payor_name, payor_account_num, total_slips, total_amount, tax_code, payload_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(submission_ref) DO UPDATE SET
                transmitter_name=excluded.transmitter_name,
                contact_email=excluded.contact_email,
                payor_name=excluded.payor_name,
                payor_account_num=excluded.payor_account_num,
                total_slips=excluded.total_slips,
                total_amount=excluded.total_amount,
                tax_code=excluded.tax_code,
                payload_hash=excluded.payload_hash
        """, (
            ref_num,
            t619.TransmitterName,
            t619.ContactEmail,
            summary.PayorName,
            summary.PayorAccountableNumber,
            summary.TotalSlips,
            summary.TotalAmount,
            tax_code,
            payload_hash
        ))
        
        cursor.execute("SELECT id FROM submissions WHERE submission_ref = ?", (ref_num,))
        submission_id = cursor.fetchone()[0]
        
        cursor.execute("DELETE FROM slips WHERE submission_id = ?", (submission_id,))
        
        slip_records = [
            (submission_id, slip.RecipientName, slip.RecipientSIN, slip.Amount)
            for slip in slips
        ]
        
        cursor.executemany("""
            INSERT INTO slips (submission_id, recipient_name, recipient_sin, amount)
            VALUES (?, ?, ?, ?)
        """, slip_records)
        
        conn.commit()
        print(f"Logged submission #{submission_id} (Ref: {ref_num}, Code: {tax_code}, Hash: {payload_hash[:8]}...) with {len(slips)} slips.")

if __name__ == "__main__":
    xml_path = "cra_submission.xml"
    model = cra_xml_to_pydantic(xml_path)
    log_submission(model, xml_file_path=xml_path, ref_num="CRA-T550-2026-001", tax_code="FED_CORP_TAX")
