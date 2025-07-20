from fastapi import FastAPI
from routers import transcript, search, create
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is up and running."}


app.include_router(transcript.router, prefix="/api/transcript")
app.include_router(search.router, prefix="/api/search")
app.include_router(create.router, prefix="/api/timestamps")




