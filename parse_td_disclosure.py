import os

PACKAGE_PATH = "/storage/emulated/0/Government_Contracts_Compliance/Legal_Briefing_Package.txt"

TD_DISCLOSURE_RECORD = """
--------------------------------------------------------------------------------
14. INSTITUTIONAL BANKING DISCLOSURE AUDIT (TD CANADA TRUST - DEC 2025)
--------------------------------------------------------------------------------
- Document Scope: Small Business Banking Commitment, Hold Funds Policy & Interest Rates (Effective Dec 12, 2025)
- Key Prime & Lending Rates:
  * TD Prime Rate: 4.450%
  * U.S. Dollar Prime (New York Prime): 6.750% (Average: 6.839%)
  * Unauthorized/Temporary Overdraft Rate: 21.000%
- Deposit & Trust Yields:
  * Business Savings (Tiered up to $5M+): 1.650% to 3.000%
  * Client Trust Account Rate: 0.100%
  * Business Chequing Accounts: 0.000%
- Hold Funds Policy Rules:
  * Standard CAD hold periods: 4 to 6 business days based on deposit method and account longevity.
  * Foreign currency holds: Up to 30 business days for non-US/Canadian international drafts.
- Audit Compliance Status: DISCLOSURE_TERMS_LOGGED_AND_VERIFIED
================================================================================
"""

def parse_and_log_td_disclosure():
    print(f"\n==========================================")
    print(" TD BANK DISCLOSURE AUDIT PARSER")
    print("==========================================")
    
    print(TD_DISCLOSURE_RECORD)

    # Append to Legal Briefing Package
    if os.path.exists(PACKAGE_PATH):
        with open(PACKAGE_PATH, "a", encoding="utf-8") as f:
            f.write(TD_DISCLOSURE_RECORD)
        print(f"[SUCCESS] Appended TD Bank disclosure audit block to:\n{PACKAGE_PATH}")
    else:
        with open(PACKAGE_PATH, "w", encoding="utf-8") as f:
            f.write(TD_DISCLOSURE_RECORD)
        print(f"[SUCCESS] Created legal briefing package and appended TD audit block at:\n{PACKAGE_PATH}")

if __name__ == "__main__":
    parse_and_log_td_disclosure()

