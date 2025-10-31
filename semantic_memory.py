from  pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from gemini_client import get_embeddings

DATA_DIR = Path("data/chroma/semantic")
DATA_DIR.mkdir(parents=True, exist_ok=True)

client = chromadb.PersistentClient(path=str(DATA_DIR))


collection=client.get_or_create_collection(name="semantic_memory")

def update(text: str, metadata: Dict = None):
    try:
        embedding=get_embeddings(text)
        added=collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            embeddings=[embedding],
            ids=[str(collection.count()+1)]
        )
        print(f"Added to semantic memory: {added}")
    except Exception as e:
        print(f"Error updating semantic memry: {e}")
    
def query(topic:str,n_result:int=3)->List[dict]:
    query_embedding=get_embeddings(topic)
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=n_result
    )
    doc=results["documents"][0]
    distances=results["distances"][0]
    metas=results["metadatas"][0]
    return [
        {
            "document":doc,
            "metadata":meta,
            "distance":1-distance
        }
        for doc,meta,distance in zip(
             doc,metas,distances)
    ]
    