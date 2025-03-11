from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser


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

    def retrieve_and_generate_history(self, query, prompt_chain):
        """Retrieves relevant chunks and generates a response."""
        docs = self.vector_store.query(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        # prompt = f"Context:\n{context}\n\nUser Query: {prompt_chain}\n\nAnswer:"
        
        # response = self.llm.invoke(prompt)
        
        # Combine the prompt chain with the retrieved context
        full_prompt = f"{prompt_chain}\n\nContext:\n{context}"
        processing_pipeline = self.llm | StrOutputParser()
        response = processing_pipeline.invoke(full_prompt)
        return response
