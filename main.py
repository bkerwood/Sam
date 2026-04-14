from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
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
    return JSONResponse({"answer": response.message.content[0].text})

@app.get("/")
async def home():
    return FileResponse("index.html")
