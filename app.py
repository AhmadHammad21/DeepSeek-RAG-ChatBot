import streamlit as st
from src.loaders.pdf_loader import PDFLoader
from src.processors.text_processor import TextProcessor
from src.embeddings.vector_store import VectorStore
from src.retrieval.rag_pipeline import RAGPipeline
from src.utils.logger import get_logger
from src.utils.exceptions import PDFLoadError
from config.settings import (
    PDF_DIRECTORY, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, VECTOR_STORE_PATH,
    CHUNK_SIZE, CHUNK_OVERLAP
)
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
from dotenv import load_dotenv

load_dotenv()

# Set up logger
logger = get_logger(__name__)

# Custom CSS styling
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("🧠 DeepSeek RAG ChatBot")
st.caption("🚀 Your AI Assistant")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")   
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🐍 ChatBot Assistant
    - 🐞 Desaisiv
    - 📝 Health Insurance Solutions
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")
    
# Initialize RAG pipeline only once
@st.cache_resource
def initialize_rag_pipeline():
    logger.info("Loading PDFs...")
    pdf_loader = PDFLoader(PDF_DIRECTORY)
    pdf_docs = pdf_loader.load_pdfs()
    if not pdf_docs:
        raise PDFLoadError("No PDFs found in the directory.")

    logger.info("Splitting text into chunks...")
    text_processor = TextProcessor(CHUNK_SIZE, CHUNK_OVERLAP)
    documents = text_processor.split_documents(pdf_docs)

    logger.info("Storing embeddings...")
    vector_store = VectorStore(EMBEDDING_MODEL_NAME)
    vector_store.build_vector_store(documents)
    vector_store.save_vector_store(VECTOR_STORE_PATH)

    logger.info("Loading vector store...")
    vector_store.load_vector_store(VECTOR_STORE_PATH)
    rag = RAGPipeline(vector_store, model_name=LLM_MODEL_NAME)

    logger.info("Pipeline is ready.")
    return rag


# Streamlit UI
st.title("RAG PDF Chat System")

# Load the pipeline
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = initialize_rag_pipeline()


# # System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI customer support assistant. Provide concise, correct answers"
    ".Always respond in English or in Arabic."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today?"}]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

# User input
query = st.chat_input("Enter your message...")

if query:
    # Display user message
    st.session_state.message_log.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    logger.info(f"Processing query: {query}")
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        print("prompt_chain")
        print(prompt_chain)
        response = st.session_state.rag_pipeline.retrieve_and_generate_history(query, prompt_chain)

    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": response})
    
    # Rerun to update chat display
    st.rerun()
