from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pinecone import Pinecone
import os

app = FastAPI()

pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
assistant = pc.assistant.Assistant(assistant_name="sam")

@app.post("/ask")
async def ask(question: str):
    try:
        response = assistant.chat(messages=[
            {"role": "user", "content": question}
        ])
        # Handle different response formats
        content = response.message.content
        if isinstance(content, str):
            answer = content
        elif isinstance(content, list):
            answer = content[0].text
        else:
            answer = str(content)
        return JSONResponse({"answer": answer})
    except Exception as e:
        return JSONResponse({"answer": f"Error: {str(e)}"})

@app.get("/")
async def home():
    return FileResponse("index.html")
