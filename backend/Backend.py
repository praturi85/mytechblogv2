# Backend: Python (FastAPI Modularized with Authentication)

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

# routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Request
from authlib.integrations.starlette_client import OAuth
import httpx

router = APIRouter()

oauth = OAuth()
oauth.register(
    "google",
    client_id="YOUR_GOOGLE_CLIENT_ID",
    client_secret="YOUR_GOOGLE_CLIENT_SECRET",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    "linkedin",
    client_id="YOUR_LINKEDIN_CLIENT_ID",
    client_secret="YOUR_LINKEDIN_CLIENT_SECRET",
    authorize_url="https://www.linkedin.com/oauth/v2/authorization",
    access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
    client_kwargs={"scope": "r_liteprofile r_emailaddress"},
)

@router.get("/google")
async def login_via_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Authentication failed")
    return user_info

@router.get("/linkedin")
async def login_via_linkedin():
    redirect_uri = "http://localhost:8000/auth/linkedin/callback"
    linkedin_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code"
        f"&client_id=YOUR_LINKEDIN_CLIENT_ID&redirect_uri={redirect_uri}&scope=r_liteprofile%20r_emailaddress"
    )
    return {"redirect_url": linkedin_url}

@router.get("/linkedin/callback")
async def linkedin_callback(code: str):
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8000/auth/linkedin/callback",
        "client_id": "YOUR_LINKEDIN_CLIENT_ID",
        "client_secret": "YOUR_LINKEDIN_CLIENT_SECRET",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="LinkedIn authentication failed")
        token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        user_info_response = await client.get("https://api.linkedin.com/v2/me", headers=headers)
        user_email_response = await client.get(
            "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
            headers=headers,
        )

    user_info = user_info_response.json()
    user_email = user_email_response.json()
    return {"user_info": user_info, "email": user_email}

# routes/article_routes.py
from fastapi import APIRouter, HTTPException
from models.article import Article
from config.db import articles_collection
from bson import ObjectId
from utils.helper import object_id_str

router = APIRouter()

@router.get("/")
async def get_articles():
    articles = list(articles_collection.find())
    for article in articles:
        article["id"] = object_id_str(article["_id"])
        del article["_id"]
    return articles

@router.post("/")
async def create_article(article: Article):
    article_dict = article.dict()
    result = articles_collection.insert_one(article_dict)
    return {"id": object_id_str(result.inserted_id), **article_dict}

@router.get("/{article_id}")
async def get_article(article_id: str):
    article = articles_collection.find_one({"_id": ObjectId(article_id)})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    article["id"] = object_id_str(article["_id"])
    del article["_id"]
    return article

# routes/comment_routes.py
from fastapi import APIRouter
from models.comment import Comment
from config.db import comments_collection

router = APIRouter()

# Similar structure for comment routes

# models/article.py
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    author: str
    category: str
    createdAt: str
    authorAvatar: str

# models/comment.py
from pydantic import BaseModel

class Comment(BaseModel):
    article_id: str
    content: str
    author: str
    createdAt: str

# config/db.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.techblog
articles_collection = db.articles
comments_collection = db.comments

# utils/helper.py
def object_id_str(obj):
    return str(obj)

# README.md
# TechBlog Project

## Overview
TechBlog is a full-stack web application where users can create, view, and manage articles and comments. The application is built with a React frontend and a FastAPI backend.

## Features
- User authentication with Google and LinkedIn.
- Articles categorized and displayed with author details.
- Comment functionality for user interaction.
- Modular architecture for scalability.

## Backend Setup
1. Install dependencies:
    ```bash
    pip install fastapi uvicorn pymongo pydantic authlib httpx
    ```

2. Database Setup:
    - Install MongoDB locally from [MongoDB Community Edition](https://www.mongodb.com/try/download/community) or use a cloud instance (e.g., [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)).
    - Start MongoDB service locally using:
      ```bash
      mongod
      ```
    - Create a database named `techblog`:
      ```bash
      mongo
      use techblog
      ```
    - Create two collections:
      ```javascript
      db.createCollection("articles");
      db.createCollection("comments");
      ```

3. Configure Google and LinkedIn credentials in `auth_routes.py`.

4. Run the backend server:
    ```bash
    python main.py
    ```

## Frontend Setup
1. Install dependencies:
    ```bash
    npm install
    ```

2. Start the frontend server:
    ```bash
    npm start
    ```

## Endpoints
- `GET /api/articles`: Fetch all articles.
- `POST /api/articles`: Create a new article.
- `GET /api/articles/{id}`: Fetch details of an article.
- `GET /auth/google`: Redirect to Google login.
- `GET /auth/google/callback`: Handle Google login callback.
- `GET /auth/linkedin`: Redirect to LinkedIn login.
- `GET /auth/linkedin/callback`: Handle LinkedIn login callback.

## Future Enhancements
- Add categories management.
- Advanced user roles.
- Enhanced UI/UX with additional features.
