from openai import OpenAI

import mysql.connector
import os
import json
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from ..models.deepseekapi import remove_json_markers
import openai


def getKey():
    load_dotenv()
    openrouter_api_key = os.getenv("API_KEY")
    print(openrouter_api_key)
    return openrouter_api_key

db_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="kavigai"
)
cursor = db_conn.cursor()

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def text_process() :
    cursor.execute("select service_name,service_description from services_templates;")
    data = cursor.fetchall()
    print(f"fetched data : {data}")
    print(f"Length of fetched data : {len(data)}")

    texts = [doc[0].replace("\n", " ") for doc in data if isinstance(doc[0], str)]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    chunks = []
    for text in texts:
        chunks.extend(text_splitter.split_text(text))
    print(f"chunks Length: {len(chunks)}")
    print(f"chunks: {chunks}")

    docs = [Document(page_content=chunk) for chunk in chunks]
    print("LCH docs:", docs)

    db = Chroma.from_documents(docs, embedding_model, persist_directory="./chroma_db")
    return db


def doAPICall(retreived_chunk,query,fdate,tdate):
        print("Start Calling......................")
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=getKey()
            )
        
        prompt = (
                "You are an assistant specialized in generating roadmap for students and divide days for each topic to complete with given from date and to date."
                "Use only the provided roadmap context to answer the question. "
                "don't add any information connecting other websies or any other company. "
                "If there is no relevant information, respond with 'Unanswerable'. "
                "give minimum 5 points in your answer.\n\n"
                "dont repeat the answer "
                f"Context:\n{retreived_chunk}\n\nQuestion: {query}.\n from date: {fdate} to date: {tdate}.\n"
                "Provide the response in JSON . "
            )

  
        response = client.chat.completions.create(
        model="cognitivecomputations/dolphin3.0-mistral-24b:free",
        messages = [{"role": "system", "content": prompt},{"role": "user", "content": query}])

        final_response = response.choices[0].message.content.strip() 
        final_output = remove_json_markers(final_response)
        print("Final Response"+final_output)    
        return final_output
     
             

    

# Query Chroma and fetch results
def start_llm(query: str, fdate, tdate):
    vector_db = text_process()
    print("vector_db function output : ", vector_db)

  
    query_embedding = embedding_model.embed_query(query)
    docs = vector_db.similarity_search_by_vector(query_embedding)
    #print("retrieved docs:", docs)
    retreived_chunk = " ".join([d.page_content for d in docs])
    print("Length : ", len(retreived_chunk)) 
    print("retreived chunk : ", retreived_chunk) 

    api_result = doAPICall(retreived_chunk,query,fdate,tdate)
    return api_result

       

 