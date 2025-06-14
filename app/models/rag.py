import os
import time
import mysql.connector
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI

db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nandha123",
    database="goals_inter")
    
cursor = db_conn.cursor()
def get_api_key():
    load_dotenv()  
    return os.getenv("OPENROUTER_API_KEY")

openrouter_api_key = get_api_key()  
embedding_model = SentenceTransformer("all-MiniLM-L6-v2") 
chroma_client = chromadb.PersistentClient(path="./app/models/chroma_persistent_storage")  
collection = chroma_client.get_or_create_collection(name="collection_name") 
openai_client = OpenAI(api_key=openrouter_api_key, base_url="https://openrouter.ai/api/v1")

def split_text(text, chunk_size=100, chunk_overlap=5):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size  
        chunks.append(text[start:end])
        start = end - chunk_overlap 
        print(f"✅ Splitting text: {start}/{len(text)} characters processed.")
    return chunks

def process_data():
    cursor.execute("SELECT goal_template_id,goal_description FROM goals_templates")
    data = cursor.fetchall()
    print(f"Fetched data from MySQL: {data}")

    chunked_data = [
        {'id': f"doc_{doc[0]}chunk{i+1}", 'text': chunk} 
        for doc in data for i, chunk in enumerate(split_text(doc[1]))]
    for doc in chunked_data:  
        doc["embedding"] = embedding_model.encode(doc['text']).tolist()
        if doc["embedding"]: 
            collection.upsert(ids=[doc['id']], documents=[doc['text']], embeddings=[doc['embedding']])
            print(f"✅ Stored chunk {doc['id']} in ChromaDB.")
        else:
            print(f"⚠ Skipping {doc['id']} due to missing embedding.")

def query_VDB(goal, n_results=2):
    query_embedding = embedding_model.encode(goal).tolist()
    print("question emberded")
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    if not results.get("documents"):
        print("⚠ No relevant chunks found.")
        return []
    return results["documents"][0]  

def generate_response(goal, relevant_chunks, fdate, tdate):
    
        try:
            if not relevant_chunks:
                return "Unanswerable: No relevant information found."

            context = "\n".join(relevant_chunks)
            prompt = (
                "You are an assistant specialized in generating roadmap for students and divide days for each topic to complete with given from date and to date. "
                "Use only the provided roadmap context to answer the question. "
                "Don't add any information connecting other websites or any other company. "
                "If there is no relevant information, respond with 'Unanswerable'. "
                "Give minimum 5 points in your answer.\n\n"
                f"Context:\n{context}\n\nQuestion: {goal}.\nFrom date: {fdate} to date: {tdate}.\n"
                "Provide the response in JSON."
            )

            response = openai_client.chat.completions.create(
                model="cognitivecomputations/dolphin3.0-mistral-24b:free",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": goal}
                ]
            )

            ai_response = response.choices[0].message.content
            return ai_response

        except Exception as e:
            print(f"Error occurred while generating AI response: {e}")
            return "An error occurred while generating the response. Please try again later."

    

def remove_json_markers(text):
    return text.replace("json", "").replace("", "").strip()

def start_llm(goal, fdate, tdate):
    process_data()  
    print(f"✅ Querying ChromaDB with goal: {goal}")
    start_time = time.time()
    relevant_chunks = query_VDB(goal)
    print(f"Query time: {time.time() - start_time} seconds")
    print(f"✅ Retrieved {len(relevant_chunks)} relevant chunks.")
    print(fdate,tdate,goal)
    answer = generate_response(goal, relevant_chunks, fdate, tdate)  # Generate AI response
    start_time = time.time()
    print(f"AI response time: {time.time() - start_time} seconds")
    resp = remove_json_markers(answer) 
    print(resp)
    return resp

