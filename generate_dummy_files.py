import os
import random
from datetime import datetime, timedelta

BASE_DIR = os.path.expanduser("~/Treasurer_Digital_Cabinet")

CATEGORIES = {
    "Invoices": [
        "Dominion_Energy_Monthly_Bill.txt",
        "AWS_Cloud_Hosting_Invoice.txt",
        "Verizon_Business_Fiber_Invoice.txt",
        "Office_Depot_Paper_Supplies.txt"
    ],
    "Receipts": [
        "Home_Depot_Maintenance_Purchase.txt",
        "Staples_Printer_Ink_Receipt.txt",
        "Chick_fil_A_Catering_Receipt.txt",
        "Chevron_Fuel_Receipt.txt"
    ],
    "Bank_Statements": [
        "Checking_Account_Statement_Jan.txt",
        "Checking_Account_Statement_Feb.txt",
        "Savings_Account_Interest_Statement.txt",
        "Merchant_Processor_Settlement.txt"
    ],
    "Tax_Records": [
        "Form_1099_MISC_Vendor_Copy.txt",
        "Form_W9_Signed_Vendor.txt",
        "State_Sales_Tax_Filing_Q1.txt",
        "Property_Tax_Assessment_Notice.txt"
    ]
}

def generate_files():
    total_created = 0
    for category, filenames in CATEGORIES.items():
        cat_dir = os.path.join(BASE_DIR, category)
        os.makedirs(cat_dir, exist_ok=True)
        
        for filename in filenames:
            file_path = os.path.join(cat_dir, filename)
            
            # Generate sample content
            date_str = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d")
            amount = f"${random.uniform(25.00, 1500.00):.2f}"
            
            content = f"==========================================\n"
            content += f" WAVERLY MUNICIPAL DIGITAL CABINET ARCHIVE\n"
            content += f"==========================================\n"
            content += f"Category:    {category.replace('_', ' ')}\n"
            content += f"Document:    {filename}\n"
            content += f"Record Date: {date_str}\n"
            content += f"Amount:      {amount}\n"
            content += f"Status:      VERIFIED / ARCHIVED\n"
            content += f"==========================================\n"
            content += f"This is a dummy test record generated for system testing.\n"
            
            with open(file_path, "w") as f:
                f.write(content)
            
            total_created += 1
            print(f"Created dummy file: {category}/{filename}")

    print(f"\nSuccessfully generated {total_created} dummy files across all categories!")

if __name__ == "__main__":
    generate_files()
