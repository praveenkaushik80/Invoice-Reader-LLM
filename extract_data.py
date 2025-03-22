import os
import getpass
from typing import Optional, Dict, List
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

class dict_format(TypedDict):
    invoice_id: str
    date_time: str
    receiver: str
    provider: Optional[str]
    # address: str Not extracting address for privacy
    restaurant: Optional[str]
    delivery_partner: Optional[str]
    order_details: List[Dict[str, Optional[str]]]
    taxes: float
    delivery_charge: Optional[float]
    platform_fee: Optional[float]
    coupon_name: Optional[List[Dict[str, Optional[str]]]]
    discount_amount: Optional[List[Dict[float, Optional[float]]]]
    total_amount: float

def load_model():
    """Loads the Mistral AI model, prompting for an API key if not set."""
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter API key for Mistral AI: ")
        os.environ["MISTRAL_API_KEY"] = api_key

    try:
        llm = init_chat_model("mistral-large-latest", model_provider="mistralai")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        llm = None

    return llm

def load_doc(pdf_path):
    """Loads documents from a PDF file."""
    loader = PyPDFLoader(pdf_path)
    try:
        print("loading file:",pdf_path)
        docs = loader.load()
    except Exception as e:
        print(f"Error loading PDF: {e}")
        docs = []

    if not docs:
        print("No documents loaded. Exiting.")
        exit()
    
    return docs

def process_document(pdf_path, llm):
    """Processes the document and returns the result."""
    try:
        # Load documents from PDF
        docs = load_doc(pdf_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    if docs is None:
        print("Failed to load documents.")
        return None

    # Define prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Write a concise summary of the following:\\n\\n{context}")]
    )
    chain = create_stuff_documents_chain(llm, prompt)
    result = chain.invoke({"context": docs})
    return result

def convert_to_dict(pdf_path):
    llm = load_model()
    result = process_document(pdf_path, llm)
    if result is None:
        print("process_document failed")
        return None
    structured_llm = llm.with_structured_output(dict_format)
    invoice_dict = structured_llm.invoke(result)
    return invoice_dict

if __name__ == "__main__":
    pdf_path = "F:\work\Miscellaneous\Invoice-Reader-LLM\sample\sample_invoice.pdf"
    invoice_dict = convert_to_dict(pdf_path)
    print(invoice_dict)