from langchain_ollama import OllamaLLM  # ✅ Correct

# Load an Ollama model (e.g., Mistral, Llama3, DeepSeek)
llm = OllamaLLM(model="deepseek-r1:1.5b")  # Replace with "deepseek-chat" if available in Ollama

# Ask a question
response = llm.invoke("What is Retrieval-Augmented Generation (RAG)?")
print(response)
