import xml.etree.ElementTree as ET
import os

XML_PATH = "/storage/emulated/0/Government_Contracts_Compliance/nr4_sample.xml" # Update path if your XML file is named differently

def parse_nr4_xml(file_path):
    print(f"\n==========================================")
    print(" CRA NR4 XML PARSER & VALIDATOR")
    print("==========================================")
    
    if not os.path.exists(file_path):
        print(f"[INFO] Sample file not found at {file_path}.")
        print("[INFO] Please place your NR4 XML file in the compliance directory or update XML_PATH.")
        return

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print(f"[SUCCESS] Successfully parsed XML root tag: <{root.tag}>")
        
        # Scan for Summary fields
        summaries = root.findall(".//NR4SummaryType") or root.findall(".//NR4Summary")
        print(f"Found summary elements: {len(summaries)}")
        
        # Scan for Slip fields
        slips = root.findall(".//NR4SlipType") or root.findall(".//NR4Slip")
        print(f"Found slip elements: {len(slips)}")
        
        for idx, slip in enumerate(slips, 1):
            recipient_name = slip.find("RCPNT_NM")
            account_nbr = slip.find("nr_acct_nbr")
            amounts = slip.find("NR4_AMT")
            
            print(f"\n--- Slip [{idx}] ---")
            print(f"  Recipient Name: {recipient_name.text if recipient_name is not None else 'N/A'}")
            print(f"  Account Number: {account_nbr.text if account_nbr is not None else 'N/A'}")
            if amounts is not None:
                for child in amounts:
                    print(f"  {child.tag}: {child.text}")
                    
        print("==========================================")

    except Exception as e:
        print(f"[ERROR] Failed to parse XML file: {e}")

if __name__ == "__main__":
    parse_nr4_xml(XML_PATH)

