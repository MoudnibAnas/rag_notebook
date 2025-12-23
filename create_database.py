from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def create_database(pdf_folder="data", persist_directory="chroma_db"):
    """Create vector database from PDFs - 100% LOCAL"""
    
    # 1. Load PDFs
    documents = []
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_folder} folder!")
        print("Please add PDF files to the 'data' folder and run this script again.")
        return None
    
    for file in pdf_files:
        pdf_path = os.path.join(pdf_folder, file)
        print(f"Loading {file}...")
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            for page in pages:
                page.metadata["source"] = file
            documents.extend(pages)
            print(f"  - Loaded {len(pages)} pages from {file}")
        except Exception as e:
            print(f"  - Error loading {file}: {e}")
            continue
    
    if not documents:
        print("No documents were successfully loaded!")
        return None
    
    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,        # Reduced from 600 for faster processing
        chunk_overlap=50,      # Reduced from 100 for better performance
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"\nCreated {len(chunks)} chunks from {len(documents)} pages")
    
    # 3. Create embeddings (LOCAL - no API)
    print("Loading local embeddings model (this may take a moment for first time)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",  # Free, runs on CPU
        model_kwargs={'device': 'cpu'}
    )
    
    # 4. Create and save vector store
    print("Creating vector database...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()
    print(f"✅ Database saved to {persist_directory}")
    print(f"✅ Database contains {vectordb._collection.count()} documents")
    return vectordb

if __name__ == "__main__":
    print("="*60)
    print("LOCAL RAG DATABASE CREATOR")
    print("="*60)
    print("This script will process PDFs in the 'data' folder")
    print("and create a local vector database for debates.\n")
    
    result = create_database()
    
    if result:
        print("\n" + "="*60)
        print("✅ DATABASE CREATION COMPLETE!")
        print("="*60)
        print("You can now generate debates using:")
        print("python query_debate.py 'Your debate topic'")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ DATABASE CREATION FAILED!")
        print("="*60)
        print("Please check that:")
        print("1. The 'data' folder contains PDF files")
        print("2. All required packages are installed")
        print("="*60)