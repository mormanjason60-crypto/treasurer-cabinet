import os
import requests

RECEIPTS_DIR = os.path.expanduser("~/dummy_receipts")
PORTAL_URL = "http://127.0.0.1:5000/upload"

if not os.path.exists(RECEIPTS_DIR):
    print(f"Directory {RECEIPTS_DIR} does not exist. Please run make_receipts.py first.")
    exit(1)

files = [f for f in os.listdir(RECEIPTS_DIR) if f.endswith('.txt')]
print(f"Found {len(files)} receipts to upload...")

uploaded_count = 0

for filename in files:
    filepath = os.path.join(RECEIPTS_DIR, filename)
    
    # Extract company name directly from file content
    company = "Unspecified"
    with open(filepath, 'r') as f:
        for line in f:
            if "Vendor/Entity:" in line:
                company = line.split("Vendor/Entity:")[1].strip()
                break
    
    # Submit via HTTP POST to the Web Cabinet
    with open(filepath, 'rb') as f:
        response = requests.post(
            PORTAL_URL,
            data={'category': 'Receipts', 'company': company},
            files={'file': (filename, f, 'text/plain')}
        )
        
    if response.status_code == 200:
        uploaded_count += 1
        print(f"[{uploaded_count}/{len(files)}] Uploaded '{filename}' for company: {company}")
    else:
        print(f"Failed to upload {filename}: {response.status_code}")

print(f"\nSuccessfully archived all {uploaded_count} receipts into your Digital Cabinet!")
