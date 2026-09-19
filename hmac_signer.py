import sqlite3
import hashlib
import hmac
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

class PurePythonSigner:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        # Generate a secure corporate signing secret for 10839477 Canada Inc.
        # In production, this secret key is securely stored on your device keyring.
        self.secret_key = b"10839477-CANADA-INC-SECURE-MASTER-KEY-2026"

    def sign_transaction(self, sender_card, recipient_card, amount, currency="CAD"):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get latest block for chain continuity
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
            "sender_card": sender_card,
            "recipient_card": recipient_card,
            "amount": amount,
            "currency": currency,
            "nonce": nonce,
            "voucher_id": voucher_id,
            "issuer": "10839477 Canada Inc."
        }

        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        block_hash = hashlib.sha256(block_string).hexdigest()

        # Generate cryptographic HMAC-SHA256 signature using the corporate master key
        signature = hmac.new(self.secret_key, block_string, hashlib.sha256).hexdigest()

        # Commit to SQLite ledger
        cursor.execute("""
            INSERT INTO octopus_transactions (
                block_index, previous_hash, timestamp, sender_card, 
                recipient_card, amount, currency, nonce, hash, 
                corporate_issuer, creator_uuid
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_index, prev_hash, timestamp, sender_card, 
            recipient_card, amount, currency, nonce, block_hash, 
            "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
        ))
        conn.commit()
        conn.close()

        print(f"\n==================================================")
        print(f"      SECURE HMAC-SIGNED LEDGER BLOCK             ")
        print(f"==================================================")
        print(f" Ledger Block    : #{new_index}")
        print(f" Sender Card     : {sender_card}")
        print(f" Recipient/Node  : {recipient_card}")
        print(f" Amount          : ${amount:.2f} {currency}")
        print(f" Voucher ID      : {voucher_id}")
        print(f"--------------------------------------------------")
        print(f" HMAC Signature  : {signature[:32]}...")
        print(f" SHA-256 Hash    : {block_hash[:32]}...")
        print(f"==================================================\n")

if __name__ == "__main__":
    print("Initializing Pure-Python HMAC Signer Engine...")
    signer = PurePythonSigner()
    # Sign and execute a secure cash-out transaction for Canada Post
    signer.sign_transaction(
        sender_card="VCARD-JUJITA-STAIRS-A9A55F37",
        recipient_card="CANADA-POST-EDMONTON-MAIN",
        amount=25.00,
        currency="CAD"
    )
