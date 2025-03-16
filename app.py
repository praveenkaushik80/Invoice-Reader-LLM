import streamlit as st
import os
import pandas as pd
from write_to_csv import write_invoice_data_to_csv
from extract_data import convert_to_dict

def main():
    st.title("Invoice Data Extractor")

    uploaded_files = st.file_uploader("Upload Invoice PDFs", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                # Save the uploaded file temporarily
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract data from the PDF
                invoice_dict = convert_to_dict(uploaded_file.name)
                
                if invoice_dict:
                    # Write the data to CSV
                    write_invoice_data_to_csv(invoice_dict)
                    st.success(f"Data from {uploaded_file.name} extracted and saved to invoice_data.csv")
                else:
                    st.error(f"Failed to extract data from {uploaded_file.name}")

                # Remove the temporary file
                os.remove(uploaded_file.name)

            except Exception as e:
                st.error(f"An error occurred while processing {uploaded_file.name}: {e}")

    # Display the CSV file
    if os.path.exists("invoice_data.csv"):
        df = pd.read_csv("invoice_data.csv")
        st.subheader("Invoice Data")
        st.dataframe(df)
    else:
        st.info("No invoice data available. Please upload PDF invoices to extract data.")

if __name__ == "__main__":
    main()