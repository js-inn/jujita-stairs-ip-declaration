import xml.etree.ElementTree as ET
from validate_schema import SubmissionModel

def cra_xml_to_pydantic(xml_file_path: str) -> SubmissionModel:
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    
    # Strip namespace for simplified element querying
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]

    # Parse T619 Header
    t619_elem = root.find("T619")
    cntc_elem = t619_elem.find("CNTC")
    
    t619_dict = {
        "TransmitterNumber": t619_elem.findtext("trans_nbr"),
        "TransmitterName": t619_elem.findtext("trans_name"),
        "ContactName": cntc_elem.findtext("cntc_name"),
        "ContactPhone": cntc_elem.findtext("cntc_phone"),
        "ContactEmail": cntc_elem.findtext("cntc_email"),
    }

    # Parse T550 Slips & Summary
    t550_elem = root.find("T550")
    
    slips_list = []
    for slip in t550_elem.findall("T550Slip"):
        slips_list.append({
            "RecipientName": slip.findtext("rcpt_name"),
            "RecipientSIN": slip.findtext("sin"),
            "Amount": float(slip.findtext("amt")),
        })

    summary_elem = t550_elem.find("T550Summary")
    summary_dict = {
        "PayorName": summary_elem.findtext("pyr_name"),
        "PayorAccountableNumber": summary_elem.findtext("pyr_acc_num"),
        "TotalSlips": int(summary_elem.findtext("tot_slips")),
        "TotalAmount": float(summary_elem.findtext("tot_amt")),
    }

    # Assemble into Pydantic model structure
    payload = {
        "T619": t619_dict,
        "T550": {
            "Summary": summary_dict,
            "Slips": slips_list
        }
    }

    return SubmissionModel.model_validate(payload)

if __name__ == "__main__":
    model = cra_xml_to_pydantic("cra_submission.xml")
    print("Successfully Deserialized and Validated XML into Pydantic Model:\n")
    print(f"Payor Name: {model.T550.Summary.PayorName}")
    print(f"Total Amount Parsed: ${model.T550.Summary.TotalAmount:.2f}")
    print(f"Parsed Slips Count: {len(model.T550.Slips)}")
