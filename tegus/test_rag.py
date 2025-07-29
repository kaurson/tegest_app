


from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv, find_dotenv
import os

CHROMA_PATH = os.getenv("RAG_MODEL_CHROMA_DATABASE_PATH")
DATA_PATH = os.getenv("RAG_MODEL_DATA_PATH")


load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
async def rag(query):

    embedding_function = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    # Search the database for relevant chunks
    try:
        results = db.similarity_search_with_relevance_scores(query, k=5)
        if not results or results[0][1] < 0.7:
            return [f"Unable to find matching results for '{query}'"]
        #res = [i[0].__dict__ for i in results]
        res = [{'content': i[0].__dict__, 'distance':i[1]} for i in results]
        return {"results":res}
    except Exception as e:
        return [f"Error occurred while processing the query: {str(e)}"]


