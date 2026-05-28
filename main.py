from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routers import stocks, predict, sentiment, chat, advisor
import os

app = FastAPI(title="InvestIQ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router,    prefix="/api")
app.include_router(predict.router,   prefix="/api")
app.include_router(sentiment.router, prefix="/api")
app.include_router(chat.router,      prefix="/api")
app.include_router(advisor.router,   prefix="/api")

# Serve the built React frontend
DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.exists(DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST, "assets")), name="assets")

    @app.get("/")
    def serve_root():
        return FileResponse(os.path.join(DIST, "index.html"))

    @app.get("/{full_path:path}")
    def serve_app(full_path: str):
        file_path = os.path.join(DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(DIST, "index.html"))
else:
    @app.get("/")
    def home():
        return {"message": "InvestIQ Backend running! Build the frontend first."}
