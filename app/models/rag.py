import os
import requests
import time
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import json

# Load environment variables
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

# Initialize Sentence Transformer model (for embeddings)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Efficient embedding model

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection = chroma_client.get_or_create_collection(name="collection_name")

# Initialize OpenAI Client with OpenRouter API (for chat completions)
client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")

# Check API Connection for OpenRouter LLM
try:
    resp = client.chat.completions.create(
        model="cognitivecomputations/dolphin3.0-mistral-24b:free",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(resp.choices[0].message.content)  # Display chatbot response
except Exception as e:
    print(f"API Error: {e}")

# Function to Load Documents from Directory
def load_documents_from_directory(directory_path):
    """Load documents from a specified directory."""
    print(f"Loading documents from {directory_path}...")
    documents = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            with open(os.path.join(directory_path, filename), 'r', encoding="utf-8") as file:
                documents.append({'id': filename, 'text': file.read()})

    return documents

# Function to Split Text into Chunks
def split_text(text, chunk_size=1000, chunk_overlap=20):
    """Split text into chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# Load documents
directory_path = "./text_files"
documents = load_documents_from_directory(directory_path)
print(f"Loaded {len(documents)} documents from {directory_path}.")

# Split documents into smaller chunks
chunked_documents = []
for doc in documents:
    chunks = split_text(doc['text'])
    print("Splitting documents...")
    for i, chunk in enumerate(chunks):
        chunked_documents.append({
            'id': f"{doc['id']}_chunk_{i+1}",
            'text': chunk
        })

print(f"Chunked documents into {len(chunked_documents)} chunks.")

# Function to Generate Embeddings
def get_embedding(text):
    try:
        embedding = embedding_model.encode(text)  # Generate embeddings locally
        print(f"Generated embedding for text: {text[:30]}...")
        return embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        time.sleep(2)  # Prevent API overuse
        return None

# Store embedded chunks in ChromaDB
for doc in chunked_documents:
    print("Generating embeddings...")
    doc["embedding"] = get_embedding(doc['text'])  # Generate embedding

    #Ensure embedding was generated before inserting into ChromaDB
    if doc["embedding"] is None:
        print(f"Skipping insertion for {doc['id']} due to missing embedding.")
        continue  # Skip documents without embeddings

    print("Inserting embedded chunks into ChromaDB")
    collection.upsert(
        ids=[doc['id']],
        documents=[doc['text']],
        embeddings=[doc['embedding']]
    )

# Function to Query ChromaDB
def query_documents(question, n_results=2):
    results = collection.query(query_texts=question, n_results=n_results)
    relevant_chunks = [doc for sublist in results['documents'] for doc in sublist]

    if not relevant_chunks:
        print("No relevant chunks found.")
    else:
        print(f"Returning relevant chunks {len(relevant_chunks)}")

    return relevant_chunks

# Function to Generate Response Using OpenRouter LLM
def generate_response(question, relevant_chunks):
    if not relevant_chunks:  #If no relevant chunks, respond with "Unanswerable"
        return "Unanswerable: No relevant information found in the document database."

    context = "\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. "
        "Use ONLY the following pieces of retrieved context to answer the question. "
        "If the context does not contain relevant information, reply with 'Unanswerable'. "
        "Keep responses concise and factual (max 3 sentences)."
        "\nContext: {context}"
        "\nQuestion: {question}"
    ).format(context=context, question=question)

    response = client.chat.completions.create(
        model="cognitivecomputations/dolphin3.0-mistral-24b:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content



def start_llm(question):
   # question = "What is a quantum computing?"
    relevant_chunks = query_documents(question)
    answer = generate_response(question, relevant_chunks)  

    # Convert answer to structured JSON format
    response_json = {
        "question": question,
        "response": answer,}

    # Print formatted JSON output
    print(json.dumps(response_json, indent=4))
    return json.dumps(response_json, indent=4)