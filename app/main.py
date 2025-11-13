import uvicorn
import shutil
import os
from fastapi import FastAPI
from app.service import ChatManager
from app.models import ChatRequest,ChatResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from fastapi.responses import FileResponse
from app.embedder import Embedder

KB_PATH = "kb"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow your frontend (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],     # allow POST/GET/OPTIONS
    allow_headers=["*"],     # allow content-type, authorization etc.
)

bot = ChatManager()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
def chat(request:ChatRequest):
    bot.add_user_message(request.message)
    reply = bot.generate_response()
    return ChatResponse(reply=reply)

@app.post("/reset")
def reset():
    bot.reset()
    return {"status":"chat memory cleared !"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs(KB_PATH, exist_ok=True)
    file_path = os.path.join(KB_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OPTIONAL: ingest only this file instead of running full pipeline
    from app.rag_ingest import ingest_file
    ingest_file(file_path)

    return {"status": "uploaded", "filename": file.filename}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)