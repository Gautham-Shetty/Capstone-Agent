import json
from pathlib import Path
from datetime import datetime,UTC


MEMORY_FILE = Path("data/memory.json")

def load_memory()->dict:
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read().strip()
                if not content:  # file is empty
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("Warning: memory.json corrupted, resetting memory.")
            return []
    return []
    
    
def save_memory(memory:dict):
    with open(MEMORY_FILE,"w") as f:
        json.dump(memory,f,indent=2)
        
def add_to_memory(event:str,content:str,metadata:dict=None):
    memory=load_memory()
    memory.append({
        "timestamp": datetime.now(UTC).isoformat(),
        "event_tye": event,
        "content":content,
        "metadata": metadata or {}
    })
    save_memory(memory)

def get_recent_memory(n:int=5) -> list:
    memory=load_memory()
    return memory[-n:]


