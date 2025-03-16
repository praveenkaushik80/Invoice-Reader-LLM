import os
from extract_data import *
from write_to_csv import *
folder = "F:\work\Miscellaneous\Food Order Analyst\Invoices\Zomato"

for filename in os.listdir(folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder, filename)
        invoice_dict = convert_to_dict(pdf_path)
        write_invoice_data_to_csv(invoice_dict)