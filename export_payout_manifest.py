import sqlite3
import json
import os

DB_FILE = "corporate_ledger.db"
MANIFEST_FILE = "postal_payout_manifest.json"

def export_latest_voucher():
    if not os.path.exists(DB_FILE):
        print(f"[ERROR] Database {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch the latest transaction block
    cursor.execute("""
        SELECT block_index, timestamp, sender_card, recipient_card, 
               amount, currency, hash, corporate_issuer, creator_uuid
        FROM octopus_transactions 
        ORDER BY block_index DESC LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if not row:
        print("[ERROR] No transactions found in ledger.")
        return

    # Construct the institutional payout manifest compliant with postal gateway expectations
    payout_manifest = {
        "corporate_entity": {
            "name": row["corporate_issuer"],
            "creator_uuid": row["creator_uuid"],
            "jurisdiction": "Canada / Alberta"
        },
        "redemption_node": {
            "outlet_name": row["recipient_card"],
            "city": "Edmonton",
            "province": "AB",
            "country": "Canada"
        },
        "transaction_details": {
            "ledger_block": row["block_index"],
            "timestamp_utc": row["timestamp"],
            "source_card": row["sender_card"],
            "amount_cad": row["amount"],
            "currency": row["currency"],
            "block_sha256": row["hash"]
        },
        "instructions": (
            "Present this manifest along with authorized corporate identification "
            "for 10839477 Canada Inc. at any participating Canada Post retail counter "
            "configured for corporate cash-out disbursement."
        )
    }

    with open(MANIFEST_FILE, "w") as f:
        json.dump(payout_manifest, f, indent=4)

    print(f"\n[SUCCESS] Payout Manifest Generated Successfully!")
    print(f"--------------------------------------------------")
    print(f"File Output     : {MANIFEST_FILE}")
    print(f"Corporate Issuer: {row['corporate_issuer']}")
    print(f"Destination Node: {row['recipient_card']}")
    print(f"Payout Amount   : ${row['amount']:.2f} {row['currency']}")
    print(f"Ledger Block    : #{row['block_index']}")
    print(f"--------------------------------------------------\n")

if __name__ == "__main__":
    export_latest_voucher()
