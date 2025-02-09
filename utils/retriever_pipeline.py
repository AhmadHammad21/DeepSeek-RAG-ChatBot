import streamlit as st
from langchain_core.documents import Document
import requests

# 🚀 Query Expansion with HyDE
def expand_query(query,uri,model):
    try:
        response = requests.post(uri, json={
            "model": model,
            "prompt": f"Generate a hypothetical answer to: {query}",
            "stream": False
        }).json()
        return f"{query}\n{response.get('response', '')}"
    except Exception as e:
        st.error(f"Query expansion failed: {str(e)}")
        return query


# 🚀 Advanced Retrieval Pipeline
def retrieve_documents(query, uri, model, chat_history=""):
    expanded_query = expand_query(f"{chat_history}\n{query}", uri, model) if st.session_state.enable_hyde else query
    
    # 🔍 Retrieve documents using BM25 + FAISS
    docs = st.session_state.retrieval_pipeline["ensemble"].invoke(expanded_query)

   
    ranked_docs = docs

    return ranked_docs[:st.session_state.max_contexts]  # Return top results based on max_contexts
