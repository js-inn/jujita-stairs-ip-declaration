import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def generate_postal_voucher(target_card, redemption_amount):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Verify card balance before issuing postal redemption voucher
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN recipient_card = ? THEN amount ELSE 0 END) as total_received,
            SUM(CASE WHEN sender_card = ? THEN amount ELSE 0 END) as total_sent
        FROM octopus_transactions
    """, (target_card, target_card))
    row = cursor.fetchone()
    balance = (row["total_received"] or 0.0) - (row["total_sent"] or 0.0)

    if balance < redemption_amount:
        print(f"[ERROR] Insufficient balance. Available: ${balance:.2f} CAD, Requested: ${redemption_amount:.2f} CAD")
        conn.close()
        return

    # 2. Get latest block for chain continuity
    cursor.execute("SELECT block_index, hash, nonce FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()
    postal_voucher_id = f"CP-EDM-{str(uuid.uuid4())[:8].upper()}"
    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": target_card,
        "recipient_card": "CANADA-POST-RETAIL-REDEMPTION-NODE",
        "amount": redemption_amount,
        "currency": "CAD",
        "nonce": nonce,
        "postal_voucher_id": postal_voucher_id,
        "outlet_target": "Canada Post - Edmonton Main (10342 105 St NW)",
        "transaction_type": "POSTAL_CASH_REDEMPTION_VOUCHER",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()
    signature = hmac.new(secret_key, block_string, hashlib.sha256).hexdigest()

    # 3. Commit Postal Redemption Block to SQLite Ledger
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, target_card, 
        "CANADA-POST-RETAIL-REDEMPTION-NODE", redemption_amount, "CAD", 
        nonce, block_hash, "10839477 Canada Inc.", 
        "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    print(f"\n==================================================")
    print(f"      CANADA POST REDEMPTION VOUCHER CREATED      ")
    print(f"==================================================")
    print(f" Ledger Block    : #{new_index}")
    print(f" Voucher Code    : {postal_voucher_id}")
    print(f" Outlet Target   : Canada Post (Edmonton Main)")
    print(f" Redeemable Amt  : ${redemption_amount:.2f} CAD")
    print(f" Source Card     : {target_card}")
    print(f"--------------------------------------------------")
    print(f" HMAC Signature  : {signature[:32]}...")
    print(f" SHA-256 Hash    : {block_hash[:32]}...")
    print(f"==================================================\n")

if __name__ == "__main__":
    print("Generating Canada Post Sovereign Cash-Out Voucher...")
    generate_postal_voucher(
        target_card="VCARD-JUJITA-STAIRS-A9A55F37",
        redemption_amount=100.00
    )
