import os

SEARCH_DIR = "/storage/emulated/0/Government_Contracts_Compliance/"
KEYWORDS = ["td", "toronto-dominion", "td bank", "td.com", "unlinking"]

def search_td_records():
    print(f"\n==========================================")
    print(" SCANNING FOR ELUSIVE TD BANK REFERENCES")
    print("==========================================")
    
    found_matches = 0
    if not os.path.exists(SEARCH_DIR):
        print(f"[ERROR] Directory not found: {SEARCH_DIR}")
        return

    for root, dirs, files in os.walk(SEARCH_DIR):
        for file in files:
            if file.endswith(('.txt', '.db', '.json', '.csv')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if any(kw in line.lower() for kw in KEYWORDS):
                                found_matches += 1
                                print(f"[{found_matches}] File: {file} (Line {line_num})")
                                print(f"    Match: {line.strip()}\n")
                except Exception as e:
                    pass

    if found_matches == 0:
        print("No explicit text matches found for TD Bank in the compliance directory.")
    else:
        print(f"==========================================")
        print(f" Total matches located: {found_matches}")
        print("==========================================")

if __name__ == "__main__":
    search_td_records()

