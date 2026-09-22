import sqlite3
import re

DB_NAME = "samsung_ledger.db"
TXT_FILE = "transactions.txt"

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

def parse_and_load():
    init_db()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    new_count = 0
    try:
        with open(TXT_FILE, "r") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if not line or line.startswith("DateTime"):
                continue
                
            # Regex pattern matching the log structure: Date Time, Hash, Amount, USD, Method
            match = re.search(r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})(0x[a-fA-F0-9]{64})(\d+\.\d+)(\$\d+\.\d+)(\w+)', line)
            
            if match:
                timestamp, tx_hash, amount, value_usd, method = match.groups()
                clean_usd = float(value_usd.replace('$', ''))
                clean_amount = float(amount)
                
                cursor.execute("SELECT 1 FROM transactions WHERE tx_hash = ?", (tx_hash,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO transactions (tx_hash, timestamp, amount, value_usd, method)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (tx_hash, timestamp, clean_amount, clean_usd, method))
                    new_count += 1
                    
        conn.commit()
        print(f"[+] Successfully parsed and logged {new_count} new transaction(s) into local database.")
        
    except Exception as e:
        print(f"[-] Error processing file: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    parse_and_load()
