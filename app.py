import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
import pandas as pd
from extract_data import convert_to_dict
from langchain.chat_models import init_chat_model

def initialize_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv('MISTRAL_API_KEY', '')
    if 'temp_csv' not in st.session_state:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        st.session_state.temp_csv = temp_file.name
        temp_file.close()
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = []
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()

def sidebar_config():
    with st.sidebar:
        st.title("🔑 API Configuration")
        
        # API Key input
        api_key = st.text_input(
            "MISTRAL API Key",
            type="password",
            value=st.session_state.api_key,
            key="api_key_input"
        )
        
        if api_key:
            os.environ["MISTRAL_API_KEY"] = api_key
            st.session_state.api_key = api_key
            st.success("API Key set!")
        else:
            st.error("Please enter your Mistral API Key")
            st.stop()

def save_to_temp_csv(invoice_dict):
    try:
        df = pd.DataFrame([invoice_dict])
        if os.path.exists(st.session_state.temp_csv) and os.path.getsize(st.session_state.temp_csv) > 0:
            df.to_csv(st.session_state.temp_csv, mode='a', header=False, index=False)
        else:
            df.to_csv(st.session_state.temp_csv, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def process_file(uploaded_file):
    try:
        # Check if file was already processed
        if uploaded_file.name in st.session_state.processed_files:
            st.warning(f"File {uploaded_file.name} was already processed. Skipping...")
            return False

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_path = temp_file.name
            
        invoice_dict = convert_to_dict(temp_path)
        os.unlink(temp_path)
        
        if invoice_dict:
            if save_to_temp_csv(invoice_dict):
                st.session_state.extracted_data.append(invoice_dict)
                st.session_state.processed_files.add(uploaded_file.name)
                return True
        return False
    except Exception as e:
        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        return False

def process_files(files):
    processed = []
    for file in files:
        if file.name.endswith('.pdf'):
            if process_file(file):
                processed.append(file.name)
    return processed

def analyze_data(df):
    try:
        # Using pandas for basic statistics
        stats = {
            "Total Orders": len(df),
            "Total Revenue": df['total_amount'].sum(),
            "Average Order Value": df['total_amount'].mean(),
            "Most Common Restaurant": df['restaurant'].mode()[0],
            "Most Used Delivery Partner": df['delivery_partner'].mode()[0]
        }
        st.write("### Basic Statistics")
        col1, col2 = st.columns(2)
        for i, (key, value) in enumerate(stats.items()):
            with col1 if i % 2 == 0 else col2:
                st.metric(
                    key,
                    f"{value:.2f}" if 'Amount' in key or 'Revenue' in key else value
                )
                
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")

def load_sample_data():
    sample_path = os.path.join(os.path.dirname(__file__), "sample", "sample_invoice.pdf")
    if os.path.exists(sample_path):
        with open(sample_path, "rb") as f:
            return f.read()
    return None

class SampleFileUpload:
    def __init__(self, name, content):
        self.name = name
        self._content = content

    def getbuffer(self):
        return self._content

def main():
    st.title("📄 Invoice Data Extractor")
    initialize_session_state()
    sidebar_config()
    
    # File Upload Section
    st.write("### Upload Files")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload Invoice PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select multiple PDF files by holding Ctrl/Cmd while selecting. New data is appended to existing data."
        )
    
    with col2:
        if st.button("Try Sample Data"):
            sample_data = load_sample_data()
            if sample_data:
                # Create a proper file-like object
                uploaded_files = [SampleFileUpload("sample_invoice.pdf", sample_data)]
                st.success("Sample data loaded!")
            else:
                st.error("Sample file not found!")

    if uploaded_files:
        with st.spinner('Processing invoices...'):
            processed_files = process_files(uploaded_files)
            if processed_files:
                st.success(f"✅ Processed {len(processed_files)} files successfully")
                with st.expander("Processed Files"):
                    for file in processed_files:
                        st.text(f"✓ {file}")
    
    # Display and Analysis Section
    if os.path.exists(st.session_state.temp_csv) and os.path.getsize(st.session_state.temp_csv) > 0:
        df = pd.read_csv(st.session_state.temp_csv)
        
        # Display extracted data
        st.subheader("📊 Extracted Data")
        st.dataframe(df, use_container_width=True)
        
        # Analysis section
        st.markdown("---")
        st.subheader("📈 Data Analysis")
        analyze_data(df)
    else:
        st.info("📝 Upload PDF invoices to see extracted data and analysis")

    # Keep cleanup only when app is closing
    def handle_cleanup():
        if st.session_state.temp_csv and os.path.exists(st.session_state.temp_csv):
            try:
                os.unlink(st.session_state.temp_csv)
            except:
                pass
    
    st.session_state["_cleanup"] = handle_cleanup

if __name__ == "__main__":
    main()