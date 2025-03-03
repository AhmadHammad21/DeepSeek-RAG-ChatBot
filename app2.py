import streamlit as st
from src.loaders.pdf_loader import PDFLoader
from src.processors.text_processor import TextProcessor
from src.embeddings.vector_store import VectorStore
from src.retrieval.rag_pipeline import RAGPipeline
from src.utils.logger import get_logger
from config.settings import (
    PDF_DIRECTORY, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, VECTOR_STORE_PATH,
    CHUNK_SIZE, CHUNK_OVERLAP
)

# Set up logger
logger = get_logger(__name__)

# Initialize the RAG pipeline
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
st.title("RAG PDF Query System")

# Initialize the RAG pipeline (only once)
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = initialize_rag_pipeline()

# Input text box
query = st.text_input("Enter your query:")

# Button to get the response
if st.button("Get Response"):
    if query:
        try:
            logger.info(f"Processing query: {query}")
            response = st.session_state.rag_pipeline.retrieve_and_generate(query)
            st.write(f"Response: {response}")
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            st.write("Sorry, I couldn't process your query.")