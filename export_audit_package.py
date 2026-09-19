import sqlite3
import pandas as pd
import json
from datetime import datetime

DB_FILE = "tax_audit_log.db"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_EXPORT = f"audit_export_{TIMESTAMP}.csv"
JSON_EXPORT = f"audit_export_{TIMESTAMP}.json"

def export_audit_data():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            # Query comprehensive submission and taxonomy records
            query_subs = """
                SELECT 
                    s.submission_ref,
                    s.transmitter_name,
                    s.contact_email,
                    s.payor_name,
                    s.payor_account_num,
                    s.tax_code,
                    tc.tax_description,
                    tc.jurisdiction,
                    tc.authority,
                    s.total_slips,
                    s.total_amount,
                    s.payload_hash,
                    s.created_at
                FROM submissions s
                LEFT JOIN tax_categories tc ON s.tax_code = tc.tax_code
            """
            df_subs = pd.read_sql_query(query_subs, conn)

            # Query slips with privacy masking
            query_slips = """
                SELECT 
                    s.submission_ref,
                    sl.recipient_name,
                    '***-***-' || SUBSTR(sl.recipient_sin, -3) AS masked_sin,
                    sl.amount
                FROM slips sl
                JOIN submissions s ON sl.submission_id = s.id
            """
            df_slips = pd.read_sql_query(query_slips, conn)

        if df_subs.empty:
            print("No submission records found to export.")
            return

        # 1. Export CSV summary
        df_subs.to_csv(CSV_EXPORT, index=False)

        # 2. Export nested JSON bundle
        export_payload = []
        for _, sub in df_subs.iterrows():
            sub_dict = sub.to_dict()
            slips_for_sub = df_slips[df_slips['submission_ref'] == sub['submission_ref']].to_dict(orient='records')
            sub_dict['slips'] = slips_for_sub
            export_payload.append(sub_dict)

        with open(JSON_EXPORT, 'w') as f:
            json.dump(export_payload, f, indent=2)

        print("=" * 80)
        print(" 📦 AUDIT PACKAGE EXPORT COMPLETED")
        print("=" * 80)
        print(f" CSV Manifest : {CSV_EXPORT}")
        print(f" JSON Package  : {JSON_EXPORT}")
        print("=" * 80)

    except Exception as e:
        print(f"Error exporting audit package: {e}")

if __name__ == "__main__":
    export_audit_data()
