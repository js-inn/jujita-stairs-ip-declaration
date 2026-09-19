import sqlite3
import hashlib
import json
from datetime import datetime, timezone
import uuid

DB_FILE = "corporate_ledger.db"

class PostalCashOutEngine:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row

    def get_card_balance(self, card_uid):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN recipient_card = ? THEN amount ELSE 0 END) as total_received,
                SUM(CASE WHEN sender_card = ? THEN amount ELSE 0 END) as total_sent
            FROM octopus_transactions
        """, (card_uid, card_uid))
        row = cursor.fetchone()
        received = row["total_received"] or 0.0
        sent = row["total_sent"] or 0.0
        return received - sent

    def get_latest_block(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT block_index, previous_hash, nonce, hash 
            FROM octopus_transactions 
            ORDER BY block_index DESC LIMIT 1
        """)
        return cursor.fetchone()

    def request_cash_out(self, card_uid, postal_terminal_id, amount, currency="CAD"):
        balance = self.get_card_balance(card_uid)
        if balance < amount:
            print(f"[ERROR] Insufficient funds on card {card_uid}. Available: ${balance:.2f} {currency}, Requested: ${amount:.2f} {currency}")
            return None

        latest = self.get_latest_block()
        if not latest:
            print("[ERROR] Ledger is empty.")
            return None

        new_index = latest["block_index"] + 1
        previous_hash = latest["hash"]
        new_nonce = latest["nonce"] + 1
        timestamp = datetime.now(timezone.utc).isoformat()
        voucher_uuid = str(uuid.uuid4())

        block_content = {
            "index": new_index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "sender_card": card_uid,
            "recipient_card": postal_terminal_id,
            "amount": amount,
            "currency": currency,
            "nonce": new_nonce,
            "voucher_id": voucher_uuid
        }

        block_string = json.dumps(block_content, sort_keys=True).encode("utf-8")
        new_hash = hashlib.sha256(block_string).hexdigest()

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO octopus_transactions (
                    block_index, previous_hash, timestamp, sender_card, 
                    recipient_card, amount, currency, nonce, hash, 
                    corporate_issuer, creator_uuid
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                new_index, previous_hash, timestamp, card_uid, 
                postal_terminal_id, amount, currency, new_nonce, new_hash, 
                "10839477 Canada Inc.", "e4f1b2a7-6d3c-4902-8a5e-9f7b6c5d4e1a"
            ))
            self.conn.commit()
            
            print(f"\n[SUCCESS] Cash-Out Voucher Generated Successfully!")
            print(f"--------------------------------------------------")
            print(f"Corporate Issuer : 10839477 Canada Inc.")
            print(f"Postal Terminal  : {postal_terminal_id}")
            print(f"Source Card      : {card_uid}")
            print(f"Payout Amount    : ${amount:.2f} {currency}")
            print(f"Voucher Reference: {voucher_uuid}")
            print(f"Ledger Block     : #{new_index}")
            print(f"--------------------------------------------------")
            return voucher_uuid
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to commit cash-out transaction: {e}")
            self.conn.rollback()
            return None

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    print("Initializing Canada Post Cash-Out Bridge...")
    engine = PostalCashOutEngine()
    engine.request_cash_out(
        card_uid="CARD-UID-ALPHA-99",
        postal_terminal_id="POSTAL-NODE-YEG-CP-042",
        amount=10.00,
        currency="CAD"
    )
    engine.close()
