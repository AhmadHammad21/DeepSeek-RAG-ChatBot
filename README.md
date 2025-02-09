### 🚀 **DeepSeek RAG Chatbot 3.0 – Now with GraphRAG & Chat History Integration!**  
**(100% Free, Private (No Internet), and Local PC Installation)**  


🔥 **DeepSeek + NOMIC + FAISS + Neural Reranking + HyDE + GraphRAG + Chat Memory = The Ultimate RAG Stack!**  

This chatbot enables **fast, accurate, and explainable retrieval of information** from PDFs, DOCX, and TXT files using **DeepSeek-7B**, **BM25**, **FAISS**, **Neural Reranking (Cross-Encoder)**, **GraphRAG**, and **Chat History Integration**.  

---

## **🔹 New Features in This Version**
✅ **GraphRAG Integration:** Enhances retrieval by constructing a **Knowledge Graph** from your documents, allowing for more **contextual and relational understanding**.  
✅ **Chat Memory History Awareness:** Maintains context by utilizing **chat history**, enabling more **coherent and contextually relevant responses**.  
✅ **Improved Error Handling:** Resolved issues related to **chat history clearing** and other minor bugs for a smoother user experience.  

---

## **🛠️ Installation & Setup**
### **1️⃣ Clone the Repository & Install Dependencies**
```bash
git clone 
cd DeepSeek-RAG-Chatbot
python -m venv venv
# Windows
venv/Scripts/activate
# Linux 
source myenv/bin/activate
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
2. **Hybrid Retrieval:** Combines **BM25** and **FAISS** to fetch the most relevant text.  
3. **GraphRAG Processing:** Builds a **Knowledge Graph** from documents to understand relationships and context.  
4. **Neural Reranking:** Utilizes **Cross-Encoder** to refine search results for higher accuracy.  
5. **Query Expansion (HyDE):** Enhances recall by generating expanded queries.  
6. **Chat Memory History Integration:** Maintains context by referencing previous interactions.  
7. **DeepSeek-7B Generation:** Produces answers based on the best-matched document chunks.  

---

## **🔹 Why This Upgrade?**
| Feature | Previous Version | New Version |
|---------|------------------|-------------|
| **Retrieval Method** | Hybrid (BM25 + FAISS) | Hybrid + **GraphRAG** |
| **Contextual Understanding** | Limited | **Enhanced with Knowledge Graphs** |
| **User Interface** | Standard | **Dark Theme with Customizable Sidebar** |
| **Chat History** | Not Utilized | **Integrated for Contextual Responses** |
| **Error Handling** | Basic | **Improved with Bug Fixes** |

---

## **📌 Common Issues & Fixes**
💡 **Issue:** Error when clearing chat history.  
✅ **Fix:** Ensure you're using the latest version of Streamlit, as `st.experimental_rerun()` has been updated.  
```bash
pip install --upgrade streamlit
```