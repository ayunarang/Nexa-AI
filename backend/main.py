from fastapi import FastAPI
from routers import transcript, search, create
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from dotenv import load_dotenv
load_dotenv()


origins = [
    "http://localhost:5173",                   
    "http://127.0.0.1:5173",                  
    "https://go-nexa-ai.vercel.app",      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is up and running."}


app.include_router(transcript.router, prefix="/api/transcript")
app.include_router(search.router, prefix="/api/search")
app.include_router(create.router, prefix="/api/timestamps")




