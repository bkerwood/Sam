from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pinecone import Pinecone
import os

app = FastAPI()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
assistant = pc.assistant.Assistant(assistant_name="sam")

@app.post("/ask")
async def ask(question: str):
    response = assistant.chat(messages=[
        {"role": "user", "content": question}
    ])
    return {"answer": response.message.content[0].text}

@app.get("/")
async def home():
    return FileResponse("index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")  
