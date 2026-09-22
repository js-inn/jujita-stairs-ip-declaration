import xml.etree.ElementTree as ET
from xml.dom import minidom
from validate_schema import SubmissionModel

def pydantic_to_cra_xml(submission: SubmissionModel) -> str:
    # CRA Namespace and Root Element Setup
    root = ET.Element("Submission", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns": "http://www.cra-arc.gc.ca/xmlns/t619/1-0-1"
    })

    # 1. Build T619 Header
    t619_data = submission.T619
    t619_elem = ET.SubElement(root, "T619")
    
    ET.SubElement(t619_elem, "sbmt_ref_num").text = "00000001"
    ET.SubElement(t619_elem, "trans_nbr").text = t619_data.TransmitterNumber
    ET.SubElement(t619_elem, "trans_name").text = t619_data.TransmitterName
    
    cntc_elem = ET.SubElement(t619_elem, "CNTC")
    ET.SubElement(cntc_elem, "cntc_name").text = t619_data.ContactName
    ET.SubElement(cntc_elem, "cntc_phone").text = t619_data.ContactPhone
    ET.SubElement(cntc_elem, "cntc_email").text = t619_data.ContactEmail

    # 2. Build T550 Body
    t550_data = submission.T550
    t550_elem = ET.SubElement(root, "T550")

    # Slips
    for slip in t550_data.Slips:
        slip_elem = ET.SubElement(t550_elem, "T550Slip")
        ET.SubElement(slip_elem, "rcpt_name").text = slip.RecipientName
        ET.SubElement(slip_elem, "sin").text = slip.RecipientSIN
        ET.SubElement(slip_elem, "amt").text = f"{slip.Amount:.2f}"

    # Summary
    summary_data = t550_data.Summary
    sum_elem = ET.SubElement(t550_elem, "T550Summary")
    ET.SubElement(sum_elem, "pyr_name").text = summary_data.PayorName
    ET.SubElement(sum_elem, "pyr_acc_num").text = summary_data.PayorAccountableNumber
    ET.SubElement(sum_elem, "tot_slips").text = str(summary_data.TotalSlips)
    ET.SubElement(sum_elem, "tot_amt").text = f"{summary_data.TotalAmount:.2f}"

    # Pretty Print XML
    raw_xml = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(raw_xml)
    return parsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    sample_payload = {
        "T619": {
            "TransmitterNumber": "001",
            "TransmitterName": "Systems & Integration Corp",
            "ContactName": "Alex Mercer",
            "ContactPhone": "555-0199",
            "ContactEmail": "alex@example.com",
        },
        "T550": {
            "Summary": {
                "PayorName": "Enterprise Logistics Ltd",
                "PayorAccountableNumber": "ACC-9988776655",
                "TotalSlips": 2,
                "TotalAmount": 350.50,
            },
            "Slips": [
                {"RecipientName": "Jane Doe", "RecipientSIN": "123456789", "Amount": 150.25},
                {"RecipientName": "John Smith", "RecipientSIN": "987654321", "Amount": 200.25},
            ],
        },
    }

    # Validate model instance
    model_instance = SubmissionModel.model_validate(sample_payload)

    # Generate XML
    xml_output = pydantic_to_cra_xml(model_instance)

    # Save output file
    with open("cra_submission.xml", "w", encoding="utf-8") as f:
        f.write(xml_output)

    print("XML successfully generated and saved to cra_submission.xml:\n")
    print(xml_output)
