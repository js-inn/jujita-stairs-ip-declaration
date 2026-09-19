import csv
import json
import os
import sqlite3

DB_FILE = "investments_audit.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_type TEXT,
            institution TEXT,
            security_name TEXT,
            identifier TEXT,
            value_cad REAL,
            filing_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def parse_and_store_csv(csv_path, account_type):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                # Flexible field matching across different statement exports (Questrade, Scotia iTrade, Trusts, etc.)
                institution = row.get('Institution', row.get('InstitutionName', account_type))
                security_name = row.get('SecurityName', row.get('Description', row.get('Security Description', row.get('Symbol', ''))))
                identifier = row.get('Identifier', row.get('CUSIP', row.get('Symbol', '')))
                
                # Clean currency strings
                raw_val = row.get('ValueCAD', row.get('Market Value', row.get('Total', row.get('Amount', '0'))))
                if isinstance(raw_val, str):
                    raw_val = raw_val.replace('$', '').replace(',', '').strip()
                value_cad = float(raw_val) if raw_val else 0.0
                
                filing_date = row.get('FilingDate', row.get('Date', ''))

                cursor.execute('''
                    INSERT INTO investments (account_type, institution, security_name, identifier, value_cad, filing_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (account_type, institution, security_name, identifier, value_cad, filing_date))
                count += 1
                
            conn.commit()
        print(f"[SUCCESS] Audited and stored {count} records under category '{account_type}'.")
    except Exception as e:
        print(f"[ERROR] Failed to parse CSV: {e}")
    finally:
        conn.close()

def query_summary():
    if not os.path.exists(DB_FILE):
        print("No audit database found yet.")
        return
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("\n=== Investment Portfolio Audit Summary ===")
    
    # Summary by account type
    cursor.execute("SELECT account_type, COUNT(*), SUM(value_cad) FROM investments GROUP BY account_type")
    rows = cursor.fetchall()
    for acc_type, count, val in rows:
        val_str = f"${val:,.2f} CAD" if val else "$0.00 CAD"
        print(f"• {acc_type}: {count} records | Total Value: {val_str}")
        
    cursor.execute("SELECT COUNT(*), SUM(value_cad) FROM investments")
    total_count, total_value = cursor.fetchone()
    print("-" * 45)
    print(f"Total Portfolio Records: {total_count}")
    print(f"Grand Total Value: ${total_value:,.2f} CAD\n" if total_value else "Grand Total Value: $0.00 CAD\n")
    
    conn.close()

if __name__ == '__main__':
    print("Select Category to Ingest:")
    print("1. Questrade (Acc #40145061)")
    print("2. Scotia iTrade")
    print("3. RRIF Trust")
    print("4. Royalty Trust")
    print("5. Non-Profit Trust")
    print("6. View Full Summary Only")
    
    choice = input("Enter choice (1-6) or press Enter to view summary: ").strip()
    
    category_map = {
        '1': 'Questrade (40145061)',
        '2': 'Scotia iTrade',
        '3': 'RRIF Trust',
        '4': 'Royalty Trust',
        '5': 'Non-Profit Trust'
    }
    
    if choice in category_map:
        target_csv = input(f"Enter path to CSV file for {category_map[choice]}: ").strip()
        if target_csv and os.path.exists(target_csv):
            parse_and_store_csv(target_csv, category_map[choice])
        else:
            print(f"[ERROR] File path invalid or not found.")
            
    query_summary()


