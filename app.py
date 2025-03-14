import os
import getpass
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain

# Load documents from PDF
pdf_path = r"F:\work\Miscellaneous\Chatbot\invoice\Order_ID_5274762576.pdf"
loader = PyPDFLoader(pdf_path)
try:
    docs = loader.load()
except Exception as e:
    print(f"Error loading PDF: {e}")
    docs = []

if not docs:
    print("No documents loaded. Exiting.")
    exit()

# Ensure API key is set
if not os.environ.get("MISTRAL_API_KEY"):
    print('Model key not set', end='')
    os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

# Initialize Mistral LLM
llm = init_chat_model("mistral-large-latest", model_provider="mistralai")

# Define prompt
prompt = ChatPromptTemplate.from_messages(
    [("system", "Write a concise summary of the following:\\n\\n{context}")]
)

# Instantiate chain
chain = create_stuff_documents_chain(llm, prompt)

# Invoke chain
result = chain.invoke({"context": docs})
print(result)