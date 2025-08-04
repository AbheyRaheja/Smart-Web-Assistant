from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from schema import ChatRequest
from chatbot import handle_query
import os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/summary-chat")
async def summary_chat(data: ChatRequest):
    return await handle_query(data)
  
@app.get('/')   
def home():
    return {'message':'Welcome to the ChatBot About Everything Plugin'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK'
    }