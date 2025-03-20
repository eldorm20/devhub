from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, questions, discussions, answers, comments
from .database import engine, Base
from . import meilisearch_client  # Import Meilisearch client

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(questions.router)
app.include_router(discussions.router)
app.include_router(answers.router)
app.include_router(comments.router)

@app.on_event("startup")
async def startup_event():
    # Initialize Meilisearch indexes on startup
    meilisearch_client.create_indexes()