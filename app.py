import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)
from config.settings import PDF_DIRECTORY, EMBEDDING_MODEL_NAME, DEEPMODEL_NAME, TOP_K
from src.querying.pipeline import QueryPipeline

rag_pipeline = QueryPipeline(PDF_DIRECTORY, EMBEDDING_MODEL_NAME, DEEPMODEL_NAME, TOP_K)
rag_pipeline.setup()

# Custom CSS styling
st.markdown("""
<style>
    /* Existing styles */
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }
    
    /* Add these new styles for select box */
    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }
    
    .stSelectbox svg {
        fill: white !important;
    }
    
    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }
    
    /* For dropdown menu items */
    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("🧠 DeepSeek RAG ChatBot")
st.caption("🚀 Your AI Assistant")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")   
    st.divider()
    st.markdown("### Model Capabilities")
    st.markdown("""
    - 🐍 Python Expert
    - 🐞 Debugging Assistant
    - 📝 Code Documentation
    - 💡 Solution Design
    """)
    st.divider()
    st.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")

llm_engine = ChatOllama(
    model=DEEPMODEL_NAME,
    base_url="http://localhost:11434",
    temperature=0.3
)

# # System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI customer support assistant. Provide concise, correct answers"
    ".Always respond in English or in Arabic."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today?"}]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain, context):
    # Combine the prompt chain with the retrieved context
    full_prompt = f"{prompt_chain}\n\nContext:\n{context}"
    processing_pipeline = llm_engine | StrOutputParser()
    return processing_pipeline.invoke(full_prompt)

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Retrieve relevant documents using the RAG pipeline
    with st.spinner("🔍 Searching for relevant information..."):
        retrieved_context = rag_pipeline.query(user_query)
    
    # Generate AI response using the retrieved context
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain, retrieved_context)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()