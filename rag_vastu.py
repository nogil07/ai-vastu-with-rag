import os
import sys
from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
import logging
load_dotenv()

import fitz
from rapidocr_onnxruntime import RapidOCR
from langchain_core.documents import Document

def load_pdf_with_ocr(pdf_path):
    print(f"Loading {pdf_path} with OCR...")
    ocr = RapidOCR()
    doc = fitz.open(pdf_path)
    documents = []
    
    for i, page in enumerate(doc):
        # Check if page has text first
        text = page.get_text().strip()
        
        # If very little text, try OCR
        if len(text) < 50:
            try:
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                result, _ = ocr(img_data)
                if result:
                    ocr_text = "\n".join([line[1] for line in result])
                    text += "\n" + ocr_text
            except Exception as e:
                print(f"OCR failed for page {i+1}: {e}")
        
        if text.strip():
            documents.append(Document(page_content=text, metadata={"source": pdf_path, "page": i+1}))
            
    print(f"Processed {len(documents)} pages.")
    return documents

def setup_rag(pdf_paths=None):
    if pdf_paths is None:
        pdf_paths = ["vastu-for-home.pdf"]
        
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"Error: {pdf_path} not found.")
            return None, None

    print("Initializing Embeddings (may take a moment to download model)...")
    # Using a small, efficient model for local embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating/Loading Vector Store...")
    # Persist directory for the database
    persist_directory = "db"
    
    # Check if DB exists to avoid re-embedding if possible
    # We load from persist_directory directly to save huge time re-processing the OCR
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print("Found existing Vector DB, loading it directly...")
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
        print("No existing DB found, processing PDFs...")
        all_documents = []
        for pdf_path in pdf_paths:
            documents = load_pdf_with_ocr(pdf_path)
            if documents:
                all_documents.extend(documents)
        
        if not all_documents:
            print("No text extracted from any PDFs!")
            return None, None
            
        print("Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(all_documents)
        print(f"Split entirely into {len(texts)} chunks.")
        
        vectordb = Chroma.from_documents(
            documents=texts, 
            embedding=embeddings,
            persist_directory=persist_directory
        )

    print("RAG System Ready!")
    
    # Check for Gemini Key
    api_key = os.getenv("GEMINI_API_KEY")
    llm = None
    
    if api_key:
        print("Gemini API Key found. Setting up LLM capabilities.")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", google_api_key=api_key)
        
        # 1. Multi-Query Retrieval Setup
        # This makes the LLM generate variations of the user's question to pull in more comprehensive context
        logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=vectordb.as_retriever(search_kwargs={"k": 10}), 
            llm=llm
        )
        
        # 2. Advanced Prompt Engineering
        system_prompt = (
            "You are an Architectural Prompt Engineer analyzing Vastu Shastra rules and Kerala Municipality Building Rules (KPBR). "
            "Your ONLY goal is to output the final optimized AI image generation prompt based strictly on the retrieved context, user inputs, and common architectural knowledge. "
            "CRITICAL: Do not output any conversational text. Do not provide reasoning, explanations, or introductory/concluding remarks. "
            "Output ONLY the optimized image generation prompt itself, formatted clearly as a structured list of visual requirements for a 2D floor plan generator. "
            "\n\nContext:"
            "\n{context}"
            "\n\nClient's Input: {input}"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("human", system_prompt)
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        qa_chain = create_retrieval_chain(retriever_from_llm, question_answer_chain)
        return qa_chain, vectordb
    else:
        print("\nWARNING: No GEMINI_API_KEY found in .env or environment.")
        print("Running in Retrieval-Only mode (Semantic Search).")
        print("To enable LLM answers, create a .env file with GEMINI_API_KEY=AIzaSy...\n")
        return None, vectordb


def main():
    qa_chain, vectordb = setup_rag(["vastu-for-home.pdf"])
    if not vectordb:
        return

    llm = qa_chain is not None

    while True:
        query = input("\nAsk a Vastu question (or 'q' to quit): ")
        if query.lower() in ['q', 'quit', 'exit']:
            break
        
        if llm:
            try:
                result = qa_chain.invoke({"input": query})
                print("\nAnswer:", result["answer"])
                print("\nSources:")
                for doc in result["context"]:
                    print(f"- Page {doc.metadata.get('page', '?')}: {doc.page_content[:100]}...")
            except Exception as e:
                print(f"Error calling LLM: {e}")
                print("\nFalling back to Retrieval-Only mode due to LLM error...")
                docs = vectordb.similarity_search(query, k=3)
                for i, doc in enumerate(docs, 1):
                    print(f"\n--- Result {i} (Page {doc.metadata.get('page', '?')}) ---")
                    print(doc.page_content)
        else:
            # Retrieval only
            print("\nRetrieving relevant info...")
            docs = vectordb.similarity_search(query, k=3)
            for i, doc in enumerate(docs, 1):
                print(f"\n--- Result {i} (Page {doc.metadata.get('page', '?')}) ---")
                print(doc.page_content)

if __name__ == "__main__":
    main()
