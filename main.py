from src.loaders.pdf_loader import PDFLoader
from src.processors.text_processor import TextProcessor
from src.embeddings.vector_store import VectorStore
from src.retrieval.rag_pipeline import RAGPipeline
from src.utils.exceptions import PDFLoadError, QueryError
from src.utils.logger import get_logger
from config.settings import (
    PDF_DIRECTORY, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME, VECTOR_STORE_PATH,
    CHUNK_SIZE, CHUNK_OVERLAP
)


logger = get_logger(__name__)

if __name__ == "__main__":

    logger.info("Loading PDFs...")
    pdf_loader = PDFLoader(PDF_DIRECTORY)
    pdf_docs = pdf_loader.load_pdfs() 
    if not pdf_docs:
        raise PDFLoadError("No PDFs found in the directory.")

    # ✅ Step 2: Process Text
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

    logger.info("Pipeline is Ready!")
    
    query = "What is the main topic of the PDFs?"
    logger.info(f"Processing query: {query}")

    response = rag.retrieve_and_generate(query)

    logger.info(f"Response {response}")
