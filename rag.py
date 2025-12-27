"""
Minimal RAG Application - Core Logic
Fast, clean, and optimized for performance with Google Gemini Flash
"""

import os
import tempfile
from typing import List, Optional
from pathlib import Path

import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA


class RAGPipeline:
    """High-performance RAG pipeline optimized for speed and accuracy"""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize RAG pipeline with Gemini Flash and ChromaDB
        
        Args:
            persist_directory: Directory to store vector database
        """
        self.persist_directory = persist_directory
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1,  # Low temperature for concise answers
            max_tokens=500    # Limit response length
        )
        self.vectorstore = None
        self.qa_chain = None
        
        # Initialize text splitter with optimized parameters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=80,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract and clean text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Cleaned text content
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        # Clean text - remove extra whitespace and normalize
        text = ' '.join(text.split())
        return text
    
    def create_documents(self, texts: List[str], sources: List[str]) -> List[Document]:
        """
        Create LangChain documents from text and sources
        
        Args:
            texts: List of text chunks
            sources: List of source file names
            
        Returns:
            List of Document objects
        """
        documents = []
        for i, (text, source) in enumerate(zip(texts, sources)):
            doc = Document(
                page_content=text,
                metadata={
                    "source": source,
                    "chunk_id": i
                }
            )
            documents.append(doc)
        return documents
    
    def add_documents(self, pdf_paths: List[str]) -> bool:
        """
        Add new PDF documents to the vector database
        
        Args:
            pdf_paths: List of PDF file paths
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Extract text from all PDFs
            all_texts = []
            all_sources = []
            
            for pdf_path in pdf_paths:
                text = self.extract_text_from_pdf(pdf_path)
                if text.strip():
                    # Split text into chunks
                    chunks = self.text_splitter.split_text(text)
                    all_texts.extend(chunks)
                    all_sources.extend([os.path.basename(pdf_path)] * len(chunks))
            
            if not all_texts:
                return False
            
            # Create documents
            documents = self.create_documents(all_texts, all_sources)
            
            # Initialize or update vectorstore
            if self.vectorstore is None:
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory
                )
            else:
                self.vectorstore.add_documents(documents)
            
            # Persist changes
            self.vectorstore.persist()
            
            # Reinitialize QA chain
            self._setup_qa_chain()
            
            return True
            
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False
    
    def _setup_qa_chain(self):
        """Setup the QA chain with optimized prompt"""
        # Optimized prompt for concise, structured answers
        prompt_template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}

Answer concisely with bullet points when possible. Cite sources using [source: filename] format.
Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 4}  # Top-K = 4 as specified
            ),
            chain_type_kwargs={
                "prompt": PROMPT,
                "verbose": False  # Disable verbose for speed
            },
            return_source_documents=True
        )
    
    def query(self, question: str) -> dict:
        """
        Query the RAG system with a question
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer and source information
        """
        if self.qa_chain is None:
            return {
                "answer": "No documents have been uploaded yet. Please upload PDF files first.",
                "sources": []
            }
        
        try:
            # Get response from QA chain
            response = self.qa_chain({"query": question})
            
            # Extract answer and sources
            answer = response["result"]
            source_docs = response["source_documents"]
            
            # Extract source information
            sources = []
            for doc in source_docs:
                metadata = doc.metadata
                sources.append({
                    "filename": metadata.get("source", "Unknown"),
                    "chunk_id": metadata.get("chunk_id", 0),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
            
            return {
                "answer": answer,
                "sources": sources
            }
            
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "sources": []
            }
    
    def list_documents(self) -> List[str]:
        """List all documents in the vector database"""
        if self.vectorstore is None:
            return []
        
        try:
            # Get all documents
            docs = self.vectorstore.get()
            sources = set()
            
            for doc in docs["metadatas"]:
                if "source" in doc:
                    sources.add(doc["source"])
            
            return list(sources)
            
        except Exception:
            return []
    
    def clear_database(self):
        """Clear all documents from the vector database"""
        try:
            if self.vectorstore:
                # Clear all documents
                self.vectorstore.delete_collection()
                self.vectorstore = None
                self.qa_chain = None
            
            # Remove persist directory if it exists
            if os.path.exists(self.persist_directory):
                import shutil
                shutil.rmtree(self.persist_directory)
                
        except Exception as e:
            print(f"Error clearing database: {str(e)}")


def create_rag_pipeline() -> RAGPipeline:
    """Factory function to create RAG pipeline instance"""
    return RAGPipeline()