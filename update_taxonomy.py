import sqlite3

DB_FILE = "tax_audit_log.db"

TAX_TYPES = [
    # Federal
    ("FED_CORP_TAX", "Federal – Corporation Tax Payments", "Federal", "CRA"),
    ("FED_GST_HST_RET", "Federal – GST/HST Return", "Federal", "CRA"),
    ("FED_GST_HST_PAY", "Federal – GST/HST Payment", "Federal", "CRA"),
    ("FED_PERS_INST", "Federal – Personal Tax Instalments", "Federal", "CRA"),
    ("FED_PAYROLL_MTH", "Federal Payroll Deductions – Monthly", "Federal", "CRA"),
    ("FED_PAYROLL_2MTH", "Federal Payroll Deductions – Twice Monthly", "Federal", "CRA"),
    ("FED_PAYROLL_WK", "Federal Payroll Deductions – Weekly", "Federal", "CRA"),

    # Alberta
    ("AB_CORP_TAX", "Alberta Finance – Corporate Income Tax", "Alberta", "TRA"),
    ("AB_FUEL_RAIL", "Alberta Finance – Fuel Tax – Railway Companies", "Alberta", "TRA"),
    ("AB_FUEL_COLL", "Alberta Finance – Fuel Tax Collectors", "Alberta", "TRA"),
    ("AB_HEALTH_REC", "Alberta Finance – Health Costs Recovery", "Alberta", "TRA"),
    ("AB_INS_TAX", "Alberta Finance – Insurance Corporations Tax", "Alberta", "TRA"),
    ("AB_IFTA", "Alberta Finance – International Fuel Tax (IFTA)", "Alberta", "TRA"),
    ("AB_PROPANE", "Alberta Finance – Propane Tax Collectors", "Alberta", "TRA"),
    ("AB_TOBACCO", "Alberta Finance – Tobacco Tax", "Alberta", "TRA"),
    ("AB_TOURISM", "Alberta Finance – Tourism Levy", "Alberta", "TRA"),
    ("AB_UNCLAIMED", "Alberta Finance – Unclaimed Property Program", "Alberta", "TRA"),
    ("AB_SCH_BENEFIT", "Alberta School Employee Benefit Payment", "Alberta", "Education"),
    ("AB_SCH_HSA", "Alberta School Employee Health Spending Account", "Alberta", "Education"),
    ("AB_TEACH_ASSOC", "Alberta Teacher's Association Payment", "Alberta", "Education"),
    ("AB_TEACH_RETIRE", "Alberta Teacher's Retirement Payment", "Alberta", "Education"),

    # British Columbia, Nova Scotia, Ontario
    ("BC_PST", "British Columbia – Provincial Sales Tax", "British Columbia", "BC Finance"),
    ("NS_WCB", "WCB of Nova Scotia Premium", "Nova Scotia", "WCB NS"),
    ("ON_FRO", "Family Resp. Office – Ontario Payment", "Ontario", "FRO"),
    ("ON_CORP_TAX", "Ontario Corporation Tax", "Ontario", "MOF"),
    ("ON_EHT", "Ontario Employer Health Tax", "Ontario", "MOF"),

    # PEI
    ("PEI_911_FEE", "PEI – 911 Cost Recovery Fee Return", "PEI", "PEI Tax"),
    ("PEI_CAP_TAX_ANN", "PEI – Financial Corporation Capital Tax Annual", "PEI", "PEI Tax"),
    ("PEI_CAP_TAX_MTH", "PEI – Financial Corporation Capital Tax Monthly", "PEI", "PEI Tax"),
    ("PEI_FUEL_TAX", "PEI – Fuel Tax Return", "PEI", "PEI Tax"),
    ("PEI_GEOLINC", "PEI – GeoLinc Plus Payment Remittance", "PEI", "PEI Tax"),
    ("PEI_PROP_TAX", "PEI – Property Tax Payment Remittance", "PEI", "PEI Tax"),
    ("PEI_ENV_TAX", "PEI – Vendor Return – Environment Tax", "PEI", "PEI Tax"),
    ("PEI_PST", "PEI – Vendor Return – Revenue Tax (PST)", "PEI", "PEI Tax"),
    ("PEI_TOBACCO", "PEI – Wholesale Tobacco Vendors Return", "PEI", "PEI Tax"),

    # Quebec
    ("QC_CSST", "Quebec – CSST Payment", "Quebec", "Revenu Québec"),
    ("QC_SUPPORT_PAY", "Quebec Collection of Support Payments", "Quebec", "Revenu Québec"),
    ("QC_GST_QST_INST", "Quebec Combined GST + QST Instalment", "Quebec", "Revenu Québec"),
    ("QC_GST_QST_REM", "Quebec Combined GST + QST Remittance", "Quebec", "Revenu Québec"),
    ("QC_CORP_TAX", "Quebec Corporate Remittance Income Tax", "Quebec", "Revenu Québec"),
    ("QC_GST_INST", "Quebec GST Instalment", "Quebec", "Revenu Québec"),
    ("QC_GST_REM", "Quebec GST Remittance", "Quebec", "Revenu Québec"),
    ("QC_PAYROLL_QTR", "Quebec Payroll Source Deduction – Quarterly", "Quebec", "Revenu Québec"),
    ("QC_PAYROLL_MTH", "Quebec Payroll Source Deductions – Monthly", "Quebec", "Revenu Québec"),
    ("QC_PAYROLL_2MTH", "Quebec Payroll Source Deductions – Twice Monthly", "Quebec", "Revenu Québec"),
    ("QC_PAYROLL_WK", "Quebec Payroll Source Deductions – Weekly", "Quebec", "Revenu Québec"),
    ("QC_PERS_INST", "Quebec Personal Instalment Remittance", "Quebec", "Revenu Québec"),
    ("QC_QST_INST", "Quebec QST Instalment", "Quebec", "Revenu Québec"),
    ("QC_QST_REM", "Quebec QST Remittance", "Quebec", "Revenu Québec"),

    # Saskatchewan
    ("SK_CAP_TAX", "Saskatchewan Corporate Capital Tax Instalment", "Saskatchewan", "SK Finance"),
    ("SK_FUEL_10A", "Saskatchewan Fuel Tax 10A", "Saskatchewan", "SK Finance"),
    ("SK_LIQUOR", "Saskatchewan Liquor Consumption Tax", "Saskatchewan", "SK Finance"),
    ("SK_PST", "Saskatchewan Provincial Sales Tax", "Saskatchewan", "SK Finance"),
    ("SK_TOBACCO_RET", "Saskatchewan Retailer Tobacco Tax", "Saskatchewan", "SK Finance"),
    ("SK_TOBACCO_WS", "Saskatchewan Wholesale Tobacco Tax", "Saskatchewan", "SK Finance")
]

def update_schema():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # 1. Create Tax Categories Taxonomy Lookup Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tax_categories (
                tax_code TEXT PRIMARY KEY,
                tax_description TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                authority TEXT NOT NULL
            )
        ''')

        # Populate lookup table
        cursor.executemany('''
            INSERT OR REPLACE INTO tax_categories (tax_code, tax_description, jurisdiction, authority)
            VALUES (?, ?, ?, ?)
        ''', TAX_TYPES)

        # 2. Add tax_code column to submissions if it doesn't exist
        cursor.execute("PRAGMA table_info(submissions)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if "tax_code" not in columns:
            cursor.execute("ALTER TABLE submissions ADD COLUMN tax_code TEXT REFERENCES tax_categories(tax_code) DEFAULT 'FED_CORP_TAX'")
            print("Added 'tax_code' column to 'submissions' table.")

        conn.commit()
        print(f"Schema updated successfully. {len(TAX_TYPES)} tax categories registered in 'tax_categories'.")

if __name__ == "__main__":
    update_schema()
