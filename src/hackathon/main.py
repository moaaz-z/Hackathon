from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hackathon.api.repository import router as repository_router

app = FastAPI(title="AI Codebase Auditor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repository_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
