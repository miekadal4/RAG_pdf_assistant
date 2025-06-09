import hashlib
import tempfile
import streamlit as st
from streamlit_chat import message

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from langchain.chains import ConversationalRetrievalChain
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever

# Embedding model used for vectorization
EMBEDDING = "nomic-embed-text"

def enhance_query(vectorstore, mode, model):
    """
    Enhance the retriever with multi-query prompting if Enhanced Mode is enabled.
    """
    if mode:
        query_prompt = PromptTemplate(input_variables=["question"],
                                      template="""
            You are an AI language model assistant. 
            Your task is to generate three different versions of the given user question to retrieve relevant documents from a vector database.
            By generating multiple perspectives in the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search.
            Provide these alternative questions separated by newlines.
            Original question: {question}""")

        retriever = MultiQueryRetriever.from_llm(
            vectorstore.as_retriever(),
            model,
            prompt=query_prompt
        )
    else:
        retriever = vectorstore.as_retriever()

    return retriever

def initialize_pdf_rag_chain(pdf, mode, model):
    """
    Load PDF, embed content, and return a conversational retrieval chain.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf.read())
        pdf_path = tmp_file.name
    # PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = splitter.split_documents(docs)

    # Vector database and embedding.
    embeddings = OllamaEmbeddings(model=EMBEDDING)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    # Retriever
    retriever = enhance_query(vectorstore, mode, model)
    # Chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain

def on_input_change():
    """
    Handles new user input and updates chat history.
    """
    question = st.session_state.user_input
    if question:
        result = st.session_state.conversation(
            {"question": question, "chat_history": st.session_state.chat_history}
        )
        answer = result["answer"]
        st.session_state.chat_history.append((question, answer))
        st.session_state.user_input = ""

def on_clear():
    """
    Clears the chat history.
    """
    st.session_state.chat_history.clear()

def get_file_hash(file):
    """
    Generates a unique MD5 hash for the uploaded PDF file.
    """
    file.seek(0)
    file_bytes = file.read()
    file.seek(0)
    return hashlib.md5(file_bytes).hexdigest()