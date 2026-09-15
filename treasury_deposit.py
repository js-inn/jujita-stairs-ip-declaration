import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

def deposit_treasury_funds(target_card, deposit_amount):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get latest block for chain continuity
    cursor.execute("SELECT block_index, hash, nonce FROM octopus_transactions ORDER BY block_index DESC LIMIT 1")
    latest = cursor.fetchone()

    new_index = latest["block_index"] + 1
    prev_hash = latest["hash"]
    nonce = latest["nonce"] + 1
    timestamp = datetime.now(timezone.utc).isoformat()
    deposit_id = str(uuid.uuid4()).upper()
    secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    block_content = {
        "index": new_index,
        "previous_hash": prev_hash,
        "timestamp": timestamp,
        "sender_card": "CORPORATE-TREASURY-RESERVE",
        "recipient_card": target_card,
        "amount": deposit_amount,
        "currency": "CAD",
        "nonce": nonce,
        "deposit_id": deposit_id,
        "transaction_type": "TREASURY_LIQUIDITY_INJECTION",
        "issuer": "10839477 Canada Inc."
    }

    block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
    block_hash = hashlib.sha256(block_string).hexdigest()
    signature = hmac.new(secret_key, block_string, hashlib.sha256).hexdigest()

    # Commit Treasury Deposit Block to SQLite Ledger
    cursor.execute("""
        INSERT INTO octopus_transactions (
            block_index, previous_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, hash, 
            corporate_issuer, creator_uuid
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_index, prev_hash, timestamp, "CORPORATE-TREASURY-RESERVE", 
        target_card, deposit_amount, "CAD", nonce, block_hash, 
        "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
    ))
    conn.commit()
    conn.close()

    print(f"\n==================================================")
    print(f"      TREASURY LIQUIDITY INJECTION SUCCESSFUL     ")
    print(f"==================================================")
    print(f" Ledger Block    : #{new_index}")
    print(f" Source          : CORPORATE-TREASURY-RESERVE")
    print(f" Recipient Card  : {target_card}")
    print(f" Deposited Amount: ${deposit_amount:.2f} CAD")
    print(f" Deposit ID      : {deposit_id}")
    print(f"--------------------------------------------------")
    print(f" HMAC Signature  : {signature[:32]}...")
    print(f" SHA-256 Hash    : {block_hash[:32]}...")
    print(f"==================================================\n")

if __name__ == "__main__":
    print("Injecting Sovereign Corporate Treasury Funds...")
    deposit_treasury_funds(
        target_card="VCARD-JUJITA-STAIRS-A9A55F37",
        deposit_amount=500.00
    )
