import sqlite3
import requests
from datetime import datetime

DB_NAME = "samsung_ledger.db"
WALLET_ADDRESS = "0x17ad9827e8492a8c63baba84c9d84a210d37fb3e"
ETHERSCAN_API_KEY = ""

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            tx_hash TEXT PRIMARY KEY,
            timestamp TEXT,
            amount REAL,
            value_usd REAL,
            method TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_and_log_transactions():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"[*] Querying ledger for address: {WALLET_ADDRESS}")
    api_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={WALLET_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data.get("status") == "1":
            txs = data.get("result", [])
            new_count = 0
            for tx in txs:
                tx_hash = tx.get("hash")
                timestamp = datetime.utcfromtimestamp(int(tx.get("timeStamp", 0))).strftime('%Y-%m-%d %H:%M:%S')
                amount = float(tx.get("value", 0)) / 10**18
                method = "Transfer" if tx.get("input") == "0x" else "Contract Interaction"
                value_usd = amount * 2450.00
                
                cursor.execute("SELECT 1 FROM transactions WHERE tx_hash = ?", (tx_hash,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO transactions (tx_hash, timestamp, amount, value_usd, method)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tx_hash, timestamp, amount, value_usd, method))
                    new_count += 1
            conn.commit()
            print(f"[+] Success! Logged {new_count} new transaction(s).")
        else:
            print(f"[-] API Notice: {data.get('message')} -> {data.get('result')}")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fetch_and_log_transactions()
