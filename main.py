
    
import asyncio
import typer
from agents import ask_second_brain,ask_internet,ask_funny_joke
from episodic_memory import add_to_memory
from semantic_memory import update
from presideo_guardrail import redact_text
# docker run -d -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest


app=typer.Typer()


@app.command()
def ingest(text:str,tag:str="note"):
    readacted,report=redact_text(text)
    update(readacted,metadata={"tag":tag})
    print({"status":"success","redaction_report":report})

@app.command()
def ask(question:str):
    answer=ask_second_brain(question)
    print("Answer:\n",answer)
    
    
@app.command()
def memorise(event:str,text:str):
    redacted, _ = redact_text(text)
    add_to_memory(event,redacted)
    print({"status":"success to episodic memory"})
 
@app.command()   
def askout(question:str):  
    answer=ask_internet(question)
    print("Answer from web:\n",answer)
    
@app.command()
def joke():
    """Get a random funny joke using the Funny Bot agent."""
    joke = asyncio.run(ask_funny_joke())
    print("😂 Funny Bot says:\n", joke)
    
    

if __name__ == "__main__":
    app()