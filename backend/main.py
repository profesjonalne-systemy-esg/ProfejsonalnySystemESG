from fastapi import FastAPI

from app.routes import ai, auth, documents, exports, health, metrics, projects, reports

app = FastAPI(
    title="ESG Reporting Platform API",
    description="Backend dla systemu raportowania i ekstrakcji danych z plików budowlanych",
    version="0.1.0",
)

for module in (health, auth, projects, documents, ai, metrics, reports, exports):
    app.include_router(module.router)


@app.get("/")
async def root():
    return {"message": "Hello ESG!"}
