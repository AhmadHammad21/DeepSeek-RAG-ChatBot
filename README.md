### 🚀 **DeepSeek RAG Chatbot**  
**(100% Free, Private (No Internet), and Local PC Installation)**  


🔥 **DeepSeek RAG = The Ultimate RAG Stack!**  

This chatbot enables **fast, accurate, and explainable retrieval of information** from PDFs, DOCX, and TXT files using **DeepSeek-7B**, **FAISS** and **Chat History Integration**.  

---

## **🛠️ Installation & Setup**
### **1️⃣ Clone the Repository & Install Dependencies**
```bash
git clone https://github.com/AhmadHammad21/DeepSeek-RAG-ChatBot
cd DeepSeek-RAG-ChatBot
# Windows
python -m venv venv
# Linux
python3 -m venv venv
# Windows
venv/Scripts/activate
# Linux 
source venv/bin/activate
pip install -r requirements.txt
```

### **2️⃣ Download & Set Up Ollama**
on linux curl -fsSL https://ollama.com/install.sh | sh
Ollama is required to run **DeepSeek-7B** and **Nomic Embeddings** locally.  
🔗 **Download Ollama** → [https://ollama.com/](https://ollama.com/)  

Then, pull the required models:
```bash
ollama pull deepseek-r1:7b
or
ollama pull deepseek-r1:14b
ollama pull nomic-embed-text
```

### **3️⃣ Run the Chatbot**
```bash
streamlit run app.py
```
---

## **📌 How It Works**
1. **Upload Documents:** Add your PDFs, DOCX, or TXT files.  
2. **Hybrid Retrieval:** Using *FAISS** to fetch the most relevant text.   
3. **DeepSeek-7B Generation:** Produces answers based on the best-matched document chunks.  

## Enhancements:
- Chat Memory
- Remove "think" from response
- fastapi
- Add docker
- Double check the code in app.py
- Add Tests
- Make it handle other formats such as (docx, txt, PNG) not just PDFs
- NOMICS
- Neural Reranking
- HyDE
- GraphRAG