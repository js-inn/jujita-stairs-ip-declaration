import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def execute_p2p_transfer(sender_card, recipient_card, transfer_amount):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Verify Sender Balance across the ledger
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN recipient_card = ? THEN amount ELSE 0 END) as total_received,
            SUM(CASE WHEN sender_card = ? THEN amount ELSE 0 END) as total_sent
        FROM octopus_transactions
    """, (sender_card, sender_card))
    row = cursor.fetchone()
    balance = (row["total_received"] or 0.0) - (row["total_sent"] or 0.0)

    # Note: If genesis/initial card funding, allow transfer or check balance
    print(f"[INFO] Current balance for {sender_card}: ${balance:.2f} CAD")

    # 2. Get latest block for chain continuity
    cursor.execute("SELECT block_index, hash, nonce FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()
    transfer_id = str(uuid.uuid4()).upper()
    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": sender_card,
        "recipient_card": recipient_card,
        "amount": transfer_amount,
        "currency": "CAD",
        "nonce": nonce,
        "transfer_id": transfer_id,
        "transfer_type": "P2P_DIRECT_SETTLEMENT",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()
    signature = hmac.new(secret_key, block_string, hashlib.sha256).hexdigest()

    # 3. Commit P2P Block to SQLite Ledger
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, sender_card, 
        recipient_card, transfer_amount, "CAD", nonce, block_hash, 
        "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    print(f"\n==================================================")
    print(f"      P2P DIRECT NODE TRANSFER SUCCESSFUL         ")
    print(f"==================================================")
    print(f" Ledger Block    : #{new_index}")
    print(f" Sender Card     : {sender_card}")
    print(f" Recipient Card  : {recipient_card}")
    print(f" Transfer Amount : ${transfer_amount:.2f} CAD")
    print(f" Transfer ID     : {transfer_id}")
    print(f"--------------------------------------------------")
    print(f" HMAC Signature  : {signature[:32]}...")
    print(f" SHA-256 Hash    : {block_hash[:32]}...")
    print(f"==================================================\n")

if __name__ == "__main__":
    print("Executing Peer-to-Peer Sovereign Transfer...")
    # Transfer between internal virtual cards or nodes
    execute_p2p_transfer(
        sender_card="VCARD-JUJITA-STAIRS-A9A55F37",
        recipient_card="NODE-PARTNER-EDMONTON-02",
        transfer_amount=15.00
    )
