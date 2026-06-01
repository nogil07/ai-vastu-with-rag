import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Configuration for the dedicated chatbot RAG
PERSIST_DIRECTORY = "db_chatbot"
PDF_PATHS = ["vastu-for-home.pdf", "LSGD-KPBR-Amendment.pdf"]

def setup_chatbot_rag():
    """Initializes a dedicated RAG system for the chatbot using its own PDF loader."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Check if DB exists, otherwise it will be empty initially (requires ingestion)
    if not os.path.exists(PERSIST_DIRECTORY) or not os.listdir(PERSIST_DIRECTORY):
        print(f"Chatbot Vector DB not found at {PERSIST_DIRECTORY}. Ingesting documents...")
        from rag_vastu import load_pdf_with_ocr
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        all_documents = []
        for pdf_path in PDF_PATHS:
            if os.path.exists(pdf_path):
                print(f"Loading {pdf_path} for chatbot using OCR...")
                try:
                    docs = load_pdf_with_ocr(pdf_path)
                    if docs:
                        all_documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {pdf_path}: {e}")
            else:
                print(f"Warning: {pdf_path} not found.")
        
        if all_documents:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            texts = text_splitter.split_documents(all_documents)
            vectordb = Chroma.from_documents(
                documents=texts, 
                embedding=embeddings, 
                persist_directory=PERSIST_DIRECTORY
            )
        else:
            print("Warning: No documents found for chatbot RAG.")
            return None
    else:
        vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found.")
        return None

    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", google_api_key=api_key)
    retriever = vectordb.as_retriever(search_kwargs={"k": 7})

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are Vasuttan AI, a friendly, profound, and expert architectural assistant. "
         "You specialize in Kerala Panchayat Building Rules (KPBR) and Vastu Shastra. "
         "Answer the user's questions definitively. Answer ONLY from the provided context. If answer is not in context, say you don't know. "
         "to provide comprehensive advice, but strongly incorporate and quote specific metrics, "
         "rules, and dimensions from the provided retrieved context where applicable. "
         "Never say 'my knowledge base does not contain this' for standard conversational.\n\n"
         "Context:\n{context}"),
        ("human", "{question}")
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

# Singleton instance to avoid re-initializing on every request
_CHATBOT_CHAIN = None

def get_chatbot_response(query: str) -> str:
    global _CHATBOT_CHAIN
    if _CHATBOT_CHAIN is None:
        _CHATBOT_CHAIN = setup_chatbot_rag()
    
    if _CHATBOT_CHAIN:
        try:
            return _CHATBOT_CHAIN.invoke(query)
        except Exception as e:
            return f"Error: {e}"
    return "Chatbot RAG system is not properly initialized."
