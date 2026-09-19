import csv
import json
import datetime
import os
from io import StringIO

# Your raw CSV data snippet
CSV_DATA = """Transaction Hash,Status,Method,Blockno,DateTime (UTC),From,From_Nametag,To,To_Nametag,Amount,Value (USD),Txn Fee
"0x427613f4fc92d7980f75aee09002fd7cc3fa43df9cf2f99eefcc8d4cd5056f40","Success","Transfer","26000453","2026-09-17 23:20:11","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0x19b13b3fe339794e7c08d72575a496c9484eccea","","0.040466708","$98.99","0.00000644"
"0xad2a2ef3201f9a583369bf40835ee3bc0e7020df3517ccd76fcb55e43c4389fe","Success","Transfer","26000450","2026-09-17 23:19:35","0x264bd8291fae1d75db2c5f573b07faa6715997b5","Paxos 4","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0.04047315","$99.00","0.00000224"
"0xb741e6a7c98ed0dff92584f2d45ba86fb343f694d3f8b0c69ce702beba428967","Success","Transfer","25993253","2026-09-16 23:13:59","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0x19b13b3fe339794e7c08d72575a496c9484eccea","","0.018619776","$45.55","0.00000668"
"0x30a58c4b532f1af29c5f39a7a4bc98ed1c7f98edc95a09b60c08e7b9547f3a75","Success","Transfer","25993210","2026-09-16 23:05:23","0x264bd8291fae1d75db2c5f573b07faa6715997b5","Paxos 4","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0.01862646","$45.56","0.00000112"
"0xe8e711557b796292c1734694930cc22d249e0ee9bd659297b6474f461873abb5","Success","Transfer","25956174","2026-09-11 19:12:35","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0x19b13b3fe339794e7c08d72575a496c9484eccea","","0.015561252","$38.06","0.0000082"
"0x9c272a232fddaf1ff8f1e1485350c957e5a1e4eb7281dbd29018c4859502fb94","Success","Transfer","25956169","2026-09-11 19:11:35","0x264bd8291fae1d75db2c5f573b07faa6715997b5","Paxos 4","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0.01556946","$38.08","0.0000038"
"0x61bee4c89a48170a1f316b6f344f3d6b630a744e4c6a80a5e8bfe5194a229e85","Success","Transfer","25933274","2026-09-08 14:34:47","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0x19b13b3fe339794e7c08d72575a496c9484eccea","","0.02193875","$53.67","0.00002276"
"0x266af157e8af354cd3989ef5e3c97ebcfe6c3f2eb97c5177d134e24e40fb7f9f","Success","Transfer","25933266","2026-09-08 14:33:11","0x264bd8291fae1d75db2c5f573b07faa6715997b5","Paxos 4","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0.02196152","$53.72","0.00002236"
"0xc9ceb9ffe4b744d38ab26d1ded657e41075f4d548b8e49afa770bead5ce1ad7b","Success","Transfer","25879177","2026-09-01 01:35:11","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0x19b13b3fe339794e7c08d72575a496c9484eccea","","0.036231797","$88.63","0.0000068"
"0xa833aa407e2e121a506676de4dddf4d7a9c04c8cfa3f5d5a56db09c5d1a5d606","Success","Transfer","25879174","2026-09-01 01:34:35","0x264bd8291fae1d75db2c5f573b07faa6715997b5","Paxos 4","0x0b65d9e397b043e6996e837c9b1db754c5468626","","0.0362386","$88.64","0.0000023"
"""

TRACKING_FILE = 'bridge_activity.json'

def batch_import():
    f = StringIO(CSV_DATA.strip())
    reader = csv.DictReader(f)
    
    records = []
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE, 'r') as file:
                records = json.load(file)
        except Exception:
            records = []
            
    added_count = 0
    for row in reader:
        usd_val = row['Value (USD)'].replace('$', '').replace(',', '').strip()
        record = {
            "timestamp": row['DateTime (UTC)'] + "Z",
            "tx_hash": row['Transaction Hash'].strip(),
            "amount_usd": float(usd_val) if usd_val else 0.0,
            "source_network": row['From_Nametag'] if row['From_Nametag'] else f"Address {row['From'][:6]}...",
            "target_network": f"Address {row['To'][:6]}..."
        }
        records.append(record)
        added_count += 1
        
    with open(TRACKING_FILE, 'w') as file:
        json.dump(records, file, indent=2)
        
    print(f"[SUCCESS] Batch imported {added_count} transactions into {TRACKING_FILE}")

if __name__ == '__main__':
    batch_import()

