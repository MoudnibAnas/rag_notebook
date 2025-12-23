import argparse
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
import os

# DEBATE PROMPT TEMPLATE
DEBATE_TEMPLATE = """
You are an academic debate moderator. Based ONLY on the provided context, generate TWO contrasting perspectives.

CONTEXT FROM DOCUMENTS:
{context}

TOPIC: {question}

Generate with EXACT format:

PERSPECTIVE A: [Argument supporting the topic]
- Point 1 with evidence [Source: {source1}, Page {page1}]
- Point 2 with evidence [Source: {source2}, Page {page2}]

PERSPECTIVE B: [Counter-argument or contrasting view]
- Point 1 with evidence [Source: {source3}, Page {page3}]
- Point 2 with evidence [Source: {source4}, Page {page4}]

NEUTRAL SUMMARY: [Balanced synthesis of both views]

RULES:
1. Use ONLY information from context
2. Every point MUST have a citation
3. Be objective and academic
"""

def generate_debate(query_text, chroma_path="chroma_db"):
    """Generate a structured debate using local LLM"""
    
    # Check if database exists
    if not os.path.exists(chroma_path):
        return f" Error: Database not found at {chroma_path}\nPlease run 'python create_database.py' first to create the database."
    
    try:
        # 1. Load local embeddings and database
        print("Loading local embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        print("Loading vector database...")
        db = Chroma(
            persist_directory=chroma_path,
            embedding_function=embeddings
        )
        
        # 2. Search for relevant context
        print(f"Searching for relevant documents about: {query_text}")
        results = db.similarity_search_with_relevance_scores(query_text, k=1)  # Reduced from 2 to 1 for faster response
        
        if not results or len(results) == 0:
            return f" No relevant documents found for the topic: {query_text}\n\nTry:\n1. Adding more PDFs to the 'data' folder\n2. Running 'python create_database.py' again\n3. Using different search terms"
        
        print(f"Found {len(results)} relevant documents")
        
        # 3. Format context with citations (limit content length)
        context_parts = []
        for i, (doc, score) in enumerate(results):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", 1)
            # Limit content to first 500 characters for faster processing
            content_preview = doc.page_content[:300].replace('\n', ' ')  # Reduced from 500 to 300 for faster processing
            context_parts.append(f"[Document {i+1}: {source}, Page {page}]\n{content_preview}...")
            print(f"  - Using content from {source} (relevance: {score:.3f})")
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        # 4. Prepare prompt (simplified for faster processing)
        prompt_template = ChatPromptTemplate.from_template(DEBATE_TEMPLATE)
        
        # Get metadata for citations (only need 2 sources now)
        sources = [results[i][0].metadata for i in range(min(2, len(results)))]
        
        prompt = prompt_template.format(
            context=context_text,
            question=query_text,
            source1=sources[0].get("source", "Doc1"),
            page1=sources[0].get("page", 1),
            source2=sources[1].get("source", "Doc2") if len(sources) > 1 else "Doc1",
            page2=sources[1].get("page", 1) if len(sources) > 1 else 1,
            source3="Doc1",  # Simplified
            page3=1,
            source4="Doc1",  # Simplified
            page4=1
        )
        
        # 5. Generate with local LLM (Ollama)
        print("Loading local LLM (this may take a moment)...")
        try:
            llm = Ollama(
                model="mistral",  # or "llama2", "mixtral", "neural-chat"
                temperature=0.2,  # Reduced temperature for faster, more focused responses
                num_predict=256   # Reduced response length for faster generation
            )
        except Exception as e:
            # Fallback to a simple template-based response
            print(f"Ollama not available: {e}")
            print("Generating fallback response...")
            return generate_fallback_debate(query_text, results)
        
        # 6. Get response
        print("Generating debate response...")
        response = llm.invoke(prompt)
        return response
        
    except Exception as e:
        return f" Error generating debate: {e}"

def generate_fallback_debate(query_text, results):
    """Generate a simple fallback debate when Ollama is not available"""
    
    # Extract key information from results
    context_summary = []
    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", 1)
        # Take first 200 characters as summary
        content_preview = doc.page_content[:200].replace('\n', ' ')
        context_summary.append(f"Document {i+1}: {source} (Page {page}) - {content_preview}...")
    
    # Create a simple structured response
    response = f"""
PERSPECTIVE A: [Analysis based on available documents]
- Key finding from documents: {context_summary[0] if len(context_summary) > 0 else 'Document analysis pending'}
- Supporting evidence: {context_summary[1] if len(context_summary) > 1 else 'Additional evidence needed'}

PERSPECTIVE B: [Alternative interpretation]
- Different perspective: The documents suggest multiple interpretations
- Counter-evidence: {context_summary[2] if len(context_summary) > 2 else 'Further analysis required'}

NEUTRAL SUMMARY: Based on the available documents, the topic '{query_text}' appears to be related to the content found in the uploaded PDFs. For a more comprehensive analysis, please ensure Ollama is properly installed and configured with a suitable model.

NOTE: This is a simplified response. For full debate generation, please install Ollama with a local LLM model.
"""
    
    return response

def main():
    parser = argparse.ArgumentParser(description="Generate academic debate from local documents")
    parser.add_argument("topic", type=str, help="Debate topic/question")
    parser.add_argument("--db", type=str, default="chroma_db", help="Path to Chroma database")
    args = parser.parse_args()
    
    print("="*60)
    print("LOCAL RAG DEBATE GENERATOR")
    print("="*60)
    
    debate = generate_debate(args.topic, args.db)
    
    print("\n" + "="*60)
    print("ACADEMIC DEBATE GENERATION")
    print("="*60)
    print(f"Topic: {args.topic}")
    print("="*60)
    print(debate)
    print("="*60)

if __name__ == "__main__":
    main()