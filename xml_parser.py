import xml.etree.ElementTree as ET
from validate_schema import Submission

def parse_cra_xml(xml_path: str) -> Submission:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Strip namespaces for simple parsing
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]
            
    t619_elem = root.find("T619")
    t619_data = {
        "submitter_acct_num": t619_elem.findtext("sbmt_acct_num", ""),
        "transmitter_name": t619_elem.findtext("txmbr_name", ""),
        "contact_name": t619_elem.findtext("cntc_name", ""),
        "contact_phone": t619_elem.findtext("cntc_phn", ""),
        "language_code": t619_elem.findtext("lang_cd", "E"),
    }
    
    returns_data = []
    for ret in root.findall("Return"):
        t4a_oas = ret.find("T4A_OAS")
        if t4a_oas is not None:
            sum_elem = t4a_oas.find("T4A_OASSummary")
            summary_data = {
                "bn": sum_elem.findtext("bn", ""),
                "total_slips": int(sum_elem.findtext("tot_slips", "0")),
                "total_gross_pay": float(sum_elem.findtext("tot_gross_pay", "0.0")),
                "total_tax_deducted": float(sum_elem.findtext("tot_tax_ded", "0.0")),
            }
            
            slips_data = []
            for slip in t4a_oas.findall("T4A_OASSlip"):
                slips_data.append({
                    "recipient_sin": slip.findtext("sin", ""),
                    "bn": slip.findtext("bn", ""),
                    "gross_pay": float(slip.findtext("gross_pay", "0.0")),
                    "tax_deducted": float(slip.findtext("tax_ded", "0.0")),
                })
                
            returns_data.append({
                "T4A_OAS": {
                    "T4A_OASSummary": summary_data,
                    "T4A_OASSlip": slips_data
                }
            })

    payload = {
        "T619": t619_data,
        "Return": returns_data
    }
    
    return Submission.model_validate(payload)

if __name__ == "__main__":
    print("XML Parser helper initialized.")
