# mytechblogv2
mytechblogv2

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
