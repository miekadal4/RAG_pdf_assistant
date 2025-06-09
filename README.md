# 📄 Local RAG-Powered Assistant

Interact with your PDF documents using open-source large language models — **locally** and **securely**. This project leverages **Retrieval-Augmented Generation (RAG)** and **Ollama** to let you upload a PDF and chat with its contents in natural language.

> No APIs. No internet. 100% local. 100% open-source.

---

## 🚀 Key Features

- 🔍 **PDF understanding** via document chunking and embeddings
- 🧠 **Local LLMs** using [Ollama](https://ollama.com/)
- 🧩 **RAG pipeline** with Chroma vector database
- 🤖 Conversational UI using [Streamlit](https://streamlit.io/)
- ⚡ Toggle between **basic** and **enhanced** retrieval modes
- 🗂️ Automatic model + PDF change detection and re-indexing

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Streamlit** | Web UI for chatting |
| **LangChain** | LLM and RAG pipeline orchestration |
| **Ollama** | Running local LLMs (e.g., `gemma`, `qwen`) |
| **Chroma** | Vector storage and similarity search |
| **PyPDFLoader** | PDF content extraction |
| **nomic-embed-text** | Embedding model for vectorization |

---

## 🧠 Models Supported

You can run the following models locally via [Ollama](https://ollama.com/):

- **`arnold`** — A custom LLM.
- **`gemma3:4b`** — Lightweight, fast LLM from Google  
- **`qwen3:8b`** — High-performance multilingual model from Alibaba
- **`nomic-embed-text`** — A high-performing open embedding model with a large token context window
> **Note:** All models are downloaded and managed via `ollama pull`.

### 🛠️ About `arnold` (custom model)

The `arnold` model was created using a separate script (`custom_llm_arnold.py`), which defines how to:

- Load a base model (e.g., `gemma3:4b`)
- Fine-tune or modify behavior with prompt templates or adapters
- Serve it through Ollama as a personalized model

---

## 🔁 Workflow

1. **PDF Upload**: The user uploads a `.pdf` file.
2. **Document Loading**: `PyPDFLoader` extracts the content.
3. **Chunking**: Text is split into overlapping segments using `RecursiveCharacterTextSplitter`.
4. **Embedding**: Each chunk is embedded using `nomic-embed-text` locally via Ollama.
5. **Vector Store**: Chunks are stored in a `ChromaDB` instance.
6. **Retrieval**:
   - Standard: basic similarity search.
   - Enhanced: multi-query expansion for more robust semantic matching.
7. **LLM Response**: The selected LLM answers based on the retrieved chunks.
8. **Chat History**: Messages persist during the session for context.

---

## 📦 Environment Setup

All required dependencies are listed in the [`requirements.txt`](./requirements.txt) file.
