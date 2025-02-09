from src.pdf_processing.pdf_indexer import PDFEmbeddingIndexer
from src.pdf_processing.pdf_extractor import PDFExtractor
from src.querying.deepseek import DeepSeekQuery

class QueryPipeline:
    def __init__(self, pdf_dir, embedding_model_name, deepseek_model_name, top_k):
        self.pdf_extractor = PDFExtractor(pdf_dir)
        self.pdf_indexer = PDFEmbeddingIndexer(embedding_model_name)
        self.deepseek_query = DeepSeekQuery(deepseek_model_name)
        self.top_k = top_k

    def setup(self):
        documents = self.pdf_extractor.extract_text()
        self.pdf_indexer.build_index(documents)

    def query(self, question):
        question_embedding = self.pdf_indexer.embed_text(question)
        distances, indices = self.pdf_indexer.index.search(question_embedding, self.top_k)
        retrieved_text = "\n".join([self.pdf_indexer.documents[i] for i in indices[0]])
        return self.deepseek_query.query(question, retrieved_text)
