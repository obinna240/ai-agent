from fastapi import FastAPI
from orchestrator import run_all_scrapers

app = FastAPI(title="AI Deals Agent")

@app.post("/search")
async def search(profile: dict):
    results = await run_all_scrapers(profile)
    return {"results": results}

@app.get("/")
def root():
    return {"message": "AI Deals Agent running"}
