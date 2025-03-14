from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from ..utils.cleaning import remove_think_tags

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
        
        return remove_think_tags(response)

    def retrieve_and_generate_history(self, query, prompt_chain):
        """Retrieves relevant chunks and generates a response."""
        docs = self.vector_store.query(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        # prompt = f"Context:\n{context}\n\nUser Query: {prompt_chain}\n\nAnswer:"
        
        # response = self.llm.invoke(prompt)
        
        # Combine the prompt chain with the retrieved context

        system_prompt = f"""Use the chat history to maintain context:
            Chat History:
            {prompt_chain}

            Analyze the question and context through these steps:
            1. Identify key entities and relationships
            2. Resolve Contradictions between sources
            3. Integrate information from multiple contexts
            4. Answer in English if the question is is english, and in Arabic if it's Arabic

            Context:
            {context}

            Question: {query}
            Answer:"""
        
        # full_prompt = f"{prompt_chain}\n\nContext:\n{context}"
        processing_pipeline = self.llm | StrOutputParser()
        response = processing_pipeline.invoke(system_prompt)
        return remove_think_tags(response)
