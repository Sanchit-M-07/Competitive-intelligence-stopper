from fastapi import FastAPI
from app.routes import scraper, detector, llm, crm, digest, extension

app = FastAPI(title="Competitive Intelligence Tracker", version="0.1.0")

# Include routers
app.include_router(scraper.router, prefix="/scraper", tags=["scraper"])
app.include_router(detector.router, prefix="/detector", tags=["detector"])
app.include_router(llm.router, prefix="/llm", tags=["llm"])
app.include_router(crm.router, prefix="/crm", tags=["crm"])
app.include_router(digest.router, prefix="/digest", tags=["digest"])
app.include_router(extension.router, prefix="/extension", tags=["extension"])

@app.get("/")
async def root():
    return {"message": "Competitive Intelligence Tracker API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}