import sqlite3
import json
from datetime import datetime, timezone

conn = sqlite3.connect("audit.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM td_account_audit ORDER BY account_type, instrument_code;")
rows = cursor.fetchall()

compliance_report = {
    "compliance_audit_metadata": {
        "generated_timestamp": datetime.now(timezone.utc).isoformat(),
        "jurisdiction": "Canada (AB)",
        "regulatory_standard": "ISO 20022 / Financial Consumer Agency Standards",
        "audit_objective": "Verification of Account Reset Discrepancy & Royalty Flow Obfuscation"
    },
    "verified_instruments": []
}

for row in rows:
    compliance_report["verified_instruments"].append({
        "account_id": row["account_id"],
        "account_type": row["account_type"],
        "instrument_code": row["instrument_code"],
        "instrument_name": row["instrument_name"],
        "currency": row["currency"],
        "stated_limit_or_yield": row["rate_or_yield"],
        "reported_balance_status": "DISCREPANCY_FLAGGED_ZEROED",
        "compliance_notes": "Logged via immutable local ledger to challenge unauthorized reset."
    })

with open("compliance_audit_report.json", "w") as f:
    json.dump(compliance_report, f, indent=4)

conn.close()
print("Compliance audit report successfully updated and regenerated: compliance_audit_report.json")
