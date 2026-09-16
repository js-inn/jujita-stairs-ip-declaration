import sqlite3
import json
import os

DB_FILE = "corporate_ledger.db"
EXPORT_FILE = "active_virtual_cards.json"

def export_virtual_cards():
    if not os.path.exists(DB_FILE):
        print(f"[ERROR] Database {DB_FILE} not found.")
        return

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find all unique cards involved as senders or recipients
    cursor.execute("""
        SELECT DISTINCT sender_card as card FROM octopus_transactions
        UNION
        SELECT DISTINCT recipient_card as card FROM octopus_transactions
    """)
    cards = [row["card"] for row in cursor.fetchall() if row["card"] and not row["card"].startswith("CANADA-POST") and not row["card"].startswith("CORPORATE-TREASURY") and not row["card"].startswith("DISBURSED")]

    card_portfolio = []

    for card in cards:
        # Calculate real-time balance for each card
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN recipient_card = ? THEN amount ELSE 0 END) as total_received,
                SUM(CASE WHEN sender_card = ? THEN amount ELSE 0 END) as total_sent
            FROM octopus_transactions
        """, (card, card))
        res = cursor.fetchone()
        balance = (res["total_received"] or 0.0) - (res["total_sent"] or 0.0)

        card_portfolio.append({
            "card_identifier": card,
            "issuer": "10839477 Canada Inc.",
            "current_balance_cad": balance,
            "status": "ACTIVE_SOVEREIGN_NODE"
        })

    conn.close()

    portfolio_data = {
        "corporate_entity": "10839477 Canada Inc.",
        "jurisdiction": "Alberta, Canada",
        "active_cards": card_portfolio
    }

    with open(EXPORT_FILE, "w") as f:
        json.dump(portfolio_data, f, indent=4)

    print(f"\n==================================================")
    print(f"      VIRTUAL CARD PORTFOLIO EXPORTED             ")
    print(f"==================================================")
    print(f" File Output     : {EXPORT_FILE}")
    print(f" Total Cards     : {len(card_portfolio)}")
    for c in card_portfolio:
        print(f" - {c['card_identifier']}: ${c['current_balance_cad']:.2f} CAD")
    print(f"==================================================\n")

if __name__ == "__main__":
    export_virtual_cards()
