import sqlite3
import sys

DB_FILE = 'corporate_ledger.db'

def filter_ledger(search_term):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("No tables found in corporate_ledger.db.")
            return

        print(f"Searching database tables for: '{search_term}'\n")
        
        match_found = False
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in cursor.fetchall()]
            
            for col in columns:
                try:
                    query = f"SELECT * FROM {table} WHERE {col} LIKE ?"
                    cursor.execute(query, (f'%{search_term}%',))
                    rows = cursor.fetchall()
                    if rows:
                        match_found = True
                        print(f"=== Match in Table: [{table}] (Column: {col}) ===")
                        for r in rows:
                            print(r)
                        print()
                except Exception:
                    continue
                    
        if not match_found:
            print(f"No records found containing '{search_term}'.")
            
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == '__main__':
    term = sys.argv[1] if len(sys.argv) > 1 else input("Enter node ID, hash, or keyword to filter by: ")
    filter_ledger(term)

