from config.settings import PDF_DIRECTORY, EMBEDDING_MODEL_NAME, DEEPMODEL_NAME, TOP_K
from src.querying.pipeline import QueryPipeline

if __name__ == "__main__":
    pipeline = QueryPipeline(PDF_DIRECTORY, EMBEDDING_MODEL_NAME, DEEPMODEL_NAME, TOP_K)
    pipeline.setup()

    question = "What is the main topic of the documents?"
    answer = pipeline.query(question)
    print("Answer:", answer)
