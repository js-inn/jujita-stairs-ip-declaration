import sqlite3
import pandas as pd

DB_FILE = "tax_audit_log.db"

def run_report():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            # Query submissions joined with tax_categories
            query_sub = """
                SELECT 
                    s.submission_ref,
                    s.payor_name,
                    tc.jurisdiction,
                    tc.authority,
                    tc.tax_description,
                    s.total_slips,
                    s.total_amount,
                    s.payload_hash
                FROM submissions s
                LEFT JOIN tax_categories tc ON s.tax_code = tc.tax_code
            """
            df_submissions = pd.read_sql_query(query_sub, conn)
            
            # Query slips
            query_slips = """
                SELECT s.submission_ref, sl.recipient_name, sl.recipient_sin, sl.amount 
                FROM slips sl 
                JOIN submissions s ON sl.submission_id = s.id
            """
            df_slips = pd.read_sql_query(query_slips, conn)

        if df_submissions.empty:
            print("No submissions found in database.")
            return

        print("="*110)
        print(" 🏢 TAX AUDIT LOG - SUMMARY & PAYLOAD INTEGRITY")
        print("="*110)
        df_submissions['total_amount'] = df_submissions['total_amount'].apply(lambda x: f"${x:,.2f}")
        # Truncate hash for clean terminal display
        df_submissions['payload_hash'] = df_submissions['payload_hash'].apply(lambda x: f"{x[:12]}..." if x else "N/A")
        print(df_submissions.to_string(index=False))
        print("\n")

        print("="*110)
        print(" 📄 SLIPS DETAIL (PRIVACY MASKED)")
        print("="*110)
        df_slips['amount'] = df_slips['amount'].apply(lambda x: f"${x:,.2f}")
        df_slips['recipient_sin'] = df_slips['recipient_sin'].apply(lambda x: f"***-***-{x[-3:]}")
        print(df_slips.to_string(index=False))
        print("="*110)

    except Exception as e:
        print(f"Error querying database: {e}")

if __name__ == "__main__":
    run_report()
