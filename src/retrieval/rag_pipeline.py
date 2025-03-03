from langchain_ollama import OllamaLLM

class RAGPipeline:
    """Retrieves relevant chunks and generates answers using an LLM."""

    def __init__(self, vector_store, model_name):
        self.vector_store = vector_store
        self.llm = OllamaLLM(model=model_name)

    def retrieve_and_generate(self, query):
        """Retrieves relevant chunks and generates a response."""
        docs = self.vector_store.query(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"Context:\n{context}\n\nUser Query: {query}\n\nAnswer:"
        
        response = self.llm.invoke(prompt)
        
        return response
