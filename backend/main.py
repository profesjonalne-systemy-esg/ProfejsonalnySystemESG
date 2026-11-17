from fastapi import FastAPI

app = FastAPI(
    title="ESG Reporting Platform API",
    description="Backend dla systemu raportowania i ekstrakcji danych z plików budowlanych",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello ESG!"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}