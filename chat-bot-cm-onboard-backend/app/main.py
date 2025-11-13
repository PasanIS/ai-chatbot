from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.dbconnection import create_tables
from app.routers.chat import router as chat_router
from app.routers.session import router as session_router
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    debug=True,
    title="Chatbot API",
    docs_url = "/docs",
    redocs_url = "/redocs",
)


@app.on_event("startup")
def on_startup():
    create_tables()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(session_router)

# app.include_router(chat_router, prefix="", tags=["chat"])
# app.include_router(session_router, prefix="", tags=["session"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Chatbot API running"}