import sqlite3
import pandas as pd
from datetime import datetime

def process_ledger(filepath, report_output="audit_report.md"):
    print(f"[-] Loading dataset from {filepath}...")
    df = pd.read_csv(filepath)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Value (USD)"] = pd.to_numeric(df["Value (USD)"], errors="coerce")
    
    conn = sqlite3.connect("transactions.db")
    df.to_sql("ledger_transactions", conn, if_exists="replace", index=False)
    
    res = pd.read_sql("SELECT COUNT(*) as t, SUM("Value (USD)") as v, AVG("Value (USD)") as a, SUM(Amount) as tok FROM ledger_transactions", conn)
    total_txns, total_usd, avg_usd, total_token = res.iloc[0]["t"], res.iloc[0]["v"] or 0, res.iloc[0]["a"] or 0, res.iloc[0]["tok"] or 0
    
    methods_df = pd.read_sql("SELECT Method, COUNT(*) as Count, SUM("Value (USD)") as USD_Volume FROM ledger_transactions GROUP BY Method", conn)
    details_df = pd.read_sql("SELECT "Timestamp (UTC)", Method, Amount, "Value (USD)", "Transaction Hash (SHA)" FROM ledger_transactions ORDER BY "Timestamp (UTC)" DESC", conn)
    
    print(f"[-] Generating report: {report_output}...")
    content = f"# Ledger Audit Report\n\n* **Generated:** {datetime.utcnow()}\n* **Source:** {filepath}\n\n## Summary\n* **Transactions:** {total_txns}\n* **Volume:** ${total_usd:,.2f}\n\n## Methods\n```text\n{methods_df.to_string(index=False)}\n```\n\n## Details\n```text\n{details_df.to_string(index=False)}\n```\n"
    
    with open(report_output, "w") as out:
        out.write(content)
    conn.close()
    print("[-] Done.")

if __name__ == "__main__":
    process_ledger("ledger_export.csv")
