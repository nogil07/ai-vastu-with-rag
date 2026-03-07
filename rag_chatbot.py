import os
from langchain_classic.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_vastu import load_pdf_with_ocr

def setup_chatbot_rag():
    """
    Initializes a dedicated RAG chain for the interactive Vasuttan Chatbot.
    This is kept entirely separate from `rag_vastu.py` which is strictly tuned 
    for generating the DALL-E floor plan prompts.
    """
    # 1. Define the PDF sources (Vastu and KPBR)
    pdf_sources = [
        "vastu-for-home.pdf", 
        "LSGD-KPBR-Amendment.pdf"
    ]
    # 2. Setup Embeddings
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    except Exception as e:
        print(f"Chatbot failed to initialize embeddings: {e}")
        return None

    # 3. Create or load the Vector DB
    persist_directory = "db_chatbot"
    try:
        if os.path.exists(persist_directory) and os.listdir(persist_directory):
            print("Chatbot RAG: Loading existing Vector DB from cache...")
            vectordb = Chroma(
                persist_directory=persist_directory, 
                embedding_function=embeddings,
                collection_name="vasuttan_chatbot_collection"
            )
        else:
            print("Chatbot RAG: Processing PDFs (This will take 30-60 seconds on first run)...")
            all_documents = []
            for pdf_file in pdf_sources:
                if not os.path.exists(pdf_file):
                    print(f"Warning: Chatbot RAG missing {pdf_file}. It will be missing context.")
                    continue
                try:
                    docs = load_pdf_with_ocr(pdf_file)
                    if docs:
                        all_documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {pdf_file} for chatbot: {e}")
                    
            if not all_documents:
                print("Chatbot RAG failure: No documents could be parsed.")
                return None

            print("Splitting text for chatbot...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            documents = text_splitter.split_documents(all_documents)
            
            vectordb = Chroma.from_documents(
                documents, 
                embeddings,
                persist_directory=persist_directory,
                collection_name="vasuttan_chatbot_collection"
            )
            print("Chatbot RAG: Built and cached new Vector DB.")
    except Exception as e:
        print(f"Chatbot failed to create or load vector store: {e}")
        return None

    # 5. Initialize the Chatbot LLM (Gemini 2.5 Flash for conversational speed)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7, # Higher temperature for more natural conversation
    )

    # 6. Define the Conversational Prompt Template
    chatbot_template = """
    You are 'Vasuttan', a friendly, highly intelligent Architectural Assistant & Vastu Shastra expert.
    You are talking directly to a user through a chat widget on a website.
    Always be polite, concise, and helpful. Use emojis occasionally (like 🏠, 📐, or 🤞).
    
    Use the provided document context to answer questions about Kerala Municipality Building Rules (KPBR) and Vastu Shastra.
    If the context does not contain the answer, rely on your general architectural knowledge but mention that it's a general guideline.
    Keep your answers relatively short (1-3 paragraphs) since you are rendering inside a small chat UI. Format with Markdown if listing rules.

    Context:
    {context}

    User Question: {question}

    Vasuttan's Answer:
    """
    
    PROMPT = PromptTemplate(
        template=chatbot_template, 
        input_variables=["context", "question"]
    )

    # 7. Create the Retrieval Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": PROMPT}
    )

    print("✅ Chatbot RAG initialized successfully.")
    return qa_chain

if __name__ == "__main__":
    # Quick CLI test of the chatbot engine
    chain = setup_chatbot_rag()
    if chain:
        ans = chain.invoke({"query": "What is the minimum setback for the front of my house according to KPBR?"})
        print(ans["result"])
