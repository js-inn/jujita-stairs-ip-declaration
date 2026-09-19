import xmlschema
import sys
import os

SCHEMA_FILE = 'agr1.xsd'

def validate_xml_filing(xml_path):
    if not os.path.exists(SCHEMA_FILE):
        print(f"[ERROR] Schema file '{SCHEMA_FILE}' not found.")
        return
        
    if not os.path.exists(xml_path):
        print(f"[ERROR] XML file '{xml_path}' not found.")
        return

    print(f"Loading schema from {SCHEMA_FILE}...")
    try:
        schema = xmlschema.XMLSchema(SCHEMA_FILE)
    except Exception as e:
        print(f"[ERROR] Failed to compile schema: {e}")
        return

    print(f"Validating {xml_path} against AGR-1 specification...")
    
    if schema.is_valid(xml_path):
        print("[SUCCESS] XML file is fully compliant with the AGR-1 schema!")
    else:
        print("[WARNING] XML file failed validation. Details:")
        for error in schema.iter_errors(xml_path):
            print(f" - Line {error.line}: {error.message}")

if __name__ == '__main__':
    target_file = input("Enter path to XML file to validate (or press Enter for test): ").strip()
    if not target_file:
        target_file = "sample_agr1.xml"
        print(f"No file given. Creating and validating a placeholder test file: {target_file}")
        
        # Create a sample compliant XML structure for testing
        sample_xml = """<?xml version="1.0"?>
        <AGR-1SlipType>
            <Detail_Record>
                <sqnbr>123456789</sqnbr>
            </Detail_Record>
            <Slip_Record>
                <RCPNT_NM>
                    <l_nm>Stairs</l_nm>
                    <g_nm>Jujita</g_nm>
                </RCPNT_NM>
                <sqnbr>123456789</sqnbr>
                <rpt_tcd>1</rpt_tcd>
                <rcpnt_ty_ind>1</rcpnt_ty_ind>
                <sin>123456782</sin>
                <slp_cnt>1</slp_cnt>
            </Slip_Record>
        </AGR-1SlipType>
        """
        with open(target_file, 'w') as f:
            f.write(sample_xml)
            
    validate_xml_filing(target_file)

