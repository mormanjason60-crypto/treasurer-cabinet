import os
import random
from datetime import datetime, timedelta

companies = [
    ("Amazon", ["Office Chair", "Desk Lamp", "USB-C Cables", "Paper Shredder", "Wireless Mouse"]),
    ("Home Depot", ["Lumber 2x4", "Plywood Sheets", "Paint Buckets", "Cordless Drill", "HVAC Filters"]),
    ("Walmart", ["Cleaning Supplies", "Breakroom Snacks", "Bottled Water", "Trash Bags", "Paper Towels"]),
    ("Dominion Energy", ["Monthly Electric Service", "Substation Grid Utility"]),
    ("Staples", ["Copy Paper (10 Reams)", "Printer Toner Cartridges", "Pens & Highlighters", "Binder Clips"]),
    ("Verizon Wireless", ["Municipal Cell Plan", "Mobile Hotspot Data Service"]),
    ("Grainger", ["Safety Goggles", "First Aid Kit Refill", "Industrial Extension Cords", "Work Gloves"])
]

out_dir = os.path.expanduser("~/dummy_receipts")
os.makedirs(out_dir, exist_ok=True)

start_date = datetime(2026, 1, 1)

for i in range(1, 101):
    company_name, item_list = random.choice(companies)
    rand_days = random.randint(0, 270)
    receipt_date = (start_date + timedelta(days=rand_days)).strftime("%Y-%m-%d")
    receipt_id = f"REC-2026-{1000 + i}"

    selected_items = random.sample(item_list, k=random.randint(1, min(3, len(item_list))))

    subtotal = 0.0
    items_block = ""
    for item in selected_items:
        price = round(random.uniform(8.50, 180.00), 2)
        subtotal += price
        items_block += f"1x {item:<30} ${price:>6.2f}\n"

    tax = round(subtotal * 0.053, 2)
    total = round(subtotal + tax, 2)

    content = f"""===================================================
                  {company_name.upper()}                 
                  Official Purchase Receipt               
===================================================

Date: {receipt_date}
Receipt No: {receipt_id}
Vendor/Entity: {company_name}
Department: Waverly Municipal Administration

---------------------------------------------------
LINE ITEMS
---------------------------------------------------
{items_block}---------------------------------------------------
                                SUB-TOTAL: ${subtotal:>6.2f}
                                TAX (5.3%): ${tax:>6.2f}
                                -------------------
                                TOTAL:     ${total:>6.2f}

PAYMENT METHOD: Municipal Purchasing Card (P-Card)
STATUS: PAID / APPROVED FOR TREASURER ARCHIVAL
===================================================
"""
    filename = f"{receipt_date}_{company_name.replace(' ', '_')}_{receipt_id}.txt"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w") as f:
        f.write(content)

print(f"Successfully generated 100 fake receipts in: {out_dir}")
