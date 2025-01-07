# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.article_routes import router as article_router
from routes.comment_routes import router as comment_router
from routes.auth_routes import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router, prefix="/api/articles", tags=["Articles"])
app.include_router(comment_router, prefix="/api/comments", tags=["Comments"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
