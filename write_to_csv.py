import csv
#from  extract_data import result
from extract_data import *
# Store the dictionary in a CSV file
csv_file = "invoice_data.csv"

def write_invoice_data_to_csv(invoice_dict):
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header
            header = list(invoice_dict.keys())
            writer.writerow(header)

            # Write the data
            data = []
            for key in header:
                value = invoice_dict[key]
                if isinstance(value, list):
                    value = str(value)  # Convert lists to strings
                data.append(value)
            writer.writerow(data)

        print(f"Data written to {csv_file} successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    pdf_path = "F:\work\Miscellaneous\Chatbot\invoice\Order_ID_5274762576.pdf"
    invoice_dict = convert_to_dict(pdf_path)
    write_invoice_data_to_csv(invoice_dict)