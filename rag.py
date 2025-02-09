from langchain_ollama import OllamaLLM
from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import LLMChain

# Step 1: Initialize the LLM (Ollama) for generation and embeddings
llm = OllamaLLM(model="deepseek-r1:14b")  # Ollama model for generation

# Create a custom embeddings model for the RAG pipeline
embeddings_model = OllamaEmbeddings(model="deepseek-r1")  # Ollama model for embeddings

# Step 2: Prepare your dataset
# Assuming `text_chunks` is a list of text chunks (documents) you want to use for retrieval
# You need to create an FAISS index for your documents.
texts = ["Your document 1 text", "Your document 2 text", "More documents..."]  # Replace with your data

# Convert text into embeddings
embedding_vectors = embeddings_model.embed_documents(texts)

# Create a FAISS index for fast retrieval
faiss_index = FAISS.from_texts(texts, embedding_vectors)

# Step 3: Setup the Retriever
retriever = faiss_index.as_retriever()

# Step 4: Create a RAG (Retrieval-Augmented Generation) pipeline
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Step 5: Define the query and get a response
query = "What are the latest updates on AI?"
response = qa_chain.run(query)

print(response)
