import os
from extract_data import *
from write_to_csv import *

# Provide Invoices file path
folder = "F:\work\Miscellaneous\Food Order Analyst\Invoices"
for root, dirs, files in os.walk(folder):
    for filename in files:
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(root, filename)
            invoice_dict = convert_to_dict(pdf_path)
            write_invoice_data_to_csv(invoice_dict)