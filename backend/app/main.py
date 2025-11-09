from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router

app = FastAPI(title="DeepKlarity Backend")

# CORS configuration
origins = [
    "http://localhost:3000",  # React frontend URL
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
    return {"message": "Backend running successfully!"}

# Include your API router
app.include_router(api_router, prefix="/api")
