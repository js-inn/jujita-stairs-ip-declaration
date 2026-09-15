import sqlite3
import hashlib
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def generate_virtual_cashout(virtual_card_uid, payout_amount=50.00, postal_outlet="CANADA-POST-EDMONTON-MAIN"):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Verify Virtual Card Balance
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN recipient_card = ? THEN amount ELSE 0 END) as total_received,
            SUM(CASE WHEN sender_card = ? THEN amount ELSE 0 END) as total_sent
        FROM octopus_transactions
    """, (virtual_card_uid, virtual_card_uid))
    row = cursor.fetchone()
    balance = (row["total_received"] or 0.0) - (row["total_sent"] or 0.0)

    if balance < payout_amount:
        print(f"[ERROR] Insufficient balance on {virtual_card_uid}. Available: ${balance:.2f} CAD, Requested: ${payout_amount:.2f} CAD")
        conn.close()
        return

    # 2. Get latest block for chain continuity
    cursor.execute("SELECT block_index, previous_hash, nonce, hash FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()
    voucher_id = str(uuid.uuid4()).upper()

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": virtual_card_uid,
        "recipient_card": postal_outlet,
        "amount": payout_amount,
        "currency": "CAD",
        "nonce": nonce,
        "voucher_id": voucher_id,
        "redemption_type": "CANADA_POST_CASH_OUT"
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    new_hash = hashlib.sha256(block_string).hexdigest()

    # 3. Commit transaction
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, virtual_card_uid, 
        postal_outlet, payout_amount, "CAD", nonce, new_hash, 
        "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    # 4. Display the Official Payout Notice for the Postal Clerk / User
    print(f"\n==================================================")
    print(f"      10839477 CANADA INC. - CASH REDEMPTION      ")
    print(f"==================================================")
    print(f" Issuer Entity   : 10839477 Canada Inc.")
    print(f" Outlet Location : {postal_outlet}, Edmonton, AB")
    print(f" Virtual Card    : {virtual_card_uid}")
    print(f" Payout Amount   : ${payout_amount:.2f} CAD")
    print(f"--------------------------------------------------")
    print(f" VOUCHER ID      : {voucher_id}")
    print(f" LEDGER BLOCK    : #{new_index}")
    print(f" ANCHOR HASH     : {new_hash[:32]}...")
    print(f"==================================================")
    print(f" Instructions: Present this Voucher ID and valid")
    print(f" corporate credentials at any participating Canada ")
    print(f" Post retail counter to execute physical cash-out.")
    print(f"==================================================\n")

if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT recipient_card FROM octopus_transactions WHERE recipient_card LIKE 'VCARD-%' ORDER BY block_index DESC LIMIT 1")
    res = cursor.fetchone()
    conn.close()

    if res:
        vcard = res[0]
        print(f"Targeting Latest Virtual Card: {vcard}")
        generate_virtual_cashout(virtual_card_uid=vcard, payout_amount=50.00)
    else:
        print("[ERROR] No virtual card found in database.")
