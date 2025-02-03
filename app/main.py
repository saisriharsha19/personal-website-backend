from fastapi import FastAPI
from app.routes import portfolio, blog, contact

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Personal Website Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
app.include_router(blog.router, prefix="/blog", tags=["Blog"])
app.include_router(contact.router, prefix="/contact", tags=["Contact"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to my personal website backend!"}

@app.get("/status", tags=["Status"])
def get_status():
    return {"status": "OK"}