import sqlite3

# Connect to your local SQLite database
conn = sqlite3.connect("audit.db")
cursor = conn.cursor()

# Data records extracted from screenshots
records = [
    # Account Details
    ("2026-09-20 14:37:45", "8ORHJ2O", "CAD FHSA", 0.0, 0.0, 0.0, "ACCOUNT", "TD Direct Investing", "CAD", "N/A"),
    
    # Investment Savings Accounts (ISAs)
    ("2026-09-20 11:46:00", "TDB8150", "Investment Savings", None, None, None, "TDB8150", "TD Investment Savings Account (CAD)", "CAD", "Min $100 / Max $50M"),
    ("2026-09-20 11:46:00", "TDB8152", "Investment Savings", None, None, None, "TDB8152", "TD Investment Savings Account (USD)", "USD", "Min $100 / Max $50M"),
    ("2026-09-20 11:46:00", "TDB8155", "Investment Savings", None, None, None, "TDB8155", "TD Investment Savings Account (CAD)", "CAD", "Min $100 / Max $150K"),
    ("2026-09-20 11:46:00", "TDB8159", "Investment Savings", None, None, None, "TDB8159", "TD Investment Savings Account (CAD)", "CAD", "Min $100 / Max $150K"),

    # Featured Portfolios & Asset Classes
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "ABS", "Asset-Backed Securities (ABS)", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "BAIL_IN", "Bank Bail-in Bonds (Senior)", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "NVCC", "Bank NVCC (Subordinated)", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "CAN_GOV", "CAN Government Benchmarks", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "HYBRID_BOND", "Hybrid Bonds (Subordinated)", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "HYDRO_STRIP", "Hydro Quebec STRIP Ladder", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "INS_BOND", "Insurance Bonds (Subordinated)", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "ONT_STRIP", "Ontario STRIP Ladder", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "PROV_LADDER", "Provincial Bond Ladder", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "TD_CORP_CAD", "TD Core Canadian Corp. Ladder", "CAD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "TD_CORP_USD", "TD Core USD Corporate Ladder", "USD", "N/A"),
    ("2026-09-20 13:54:00", "PORTFOLIO", "Featured Portfolios", None, None, None, "US_TREASURY", "US Treasury Benchmarks", "USD", "N/A"),

    # Sample GIC Rates
    ("2026-09-20 09:39:26", "GIC", "Cashable GIC", None, None, None, "TDBK_1Y", "TDBK 1Y CSHBL NONREG (1 Year)", "CAD", "Monthly: 1.750%"),
    ("2026-09-20 09:39:26", "GIC", "Cashable GIC", None, None, None, "TDB_3Y", "TDB 3Y PREM CASH (3 Year)", "CAD", "Annual: 2.500%"),
    ("2026-09-20 09:39:26", "GIC", "Cashable GIC", None, None, None, "CTC_3Y", "CTC 3Y PREM CASH (3 Year)", "CAD", "Annual: 2.500%")
]

# Insert records into the table
cursor.executemany("""
    INSERT INTO td_account_audit (
        timestamp, account_id, account_type, total_value, 
        cash_balance, investments_value, instrument_code, 
        instrument_name, currency, rate_or_yield
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", records)

conn.commit()
print(f"Successfully inserted {cursor.rowcount} audit records into database.")

# Quick verification query
cursor.execute("SELECT count(*), account_type FROM td_account_audit GROUP BY account_type;")
for row in cursor.fetchall():
    print(f" - Category '{row[1]}': {row[0]} items logged")

conn.close()
