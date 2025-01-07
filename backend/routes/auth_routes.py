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
