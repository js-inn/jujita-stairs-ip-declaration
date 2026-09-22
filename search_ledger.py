import sqlite3
import sys

DB_FILE = 'corporate_ledger.db'

def search_tokens(query_term):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get all table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        if not tables:
            print("No tables found in the database.")
            return

        print(f"Scanning tables {tables} for '{query_term}'...\n")
        
        found_results = false = False
        for table in tables:
            # Get column names for the table
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Search each column for the target query term
            for col in columns:
                try:
                    sql = f"SELECT * FROM {table} WHERE {col} LIKE ?"
                    cursor.execute(sql, (f'%{query_term}%',))
                    rows = cursor.fetchall()
                    if rows:
                        found_results = True
                        print(f"--- Found in Table: '{table}' (Column: '{col}') ---")
                        for row in rows:
                            print(row)
                        print()
                except sqlite3.OperationalError:
                    continue
                    
        if not found_results:
            print(f"No records found matching '{query_term}'.")
            
        conn.close()
    except Exception as e:
        print(f"Error accessing database: {e}")

if __name__ == '__main__':
    term = sys.argv[1] if len(sys.argv) > 1 else input("Enter token name, symbol, or address to search: ")
    search_tokens(term)

