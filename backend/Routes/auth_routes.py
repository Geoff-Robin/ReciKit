from fastapi import APIRouter, Form, HTTPException, Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeSerializer
from passlib.context import CryptContext
import os
import hashlib
import ast
import base64

load_dotenv()
auth = APIRouter()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeSerializer(secret_key=os.getenv("SECRET_KEY"))


@auth.post("/signup")
async def signup(username: str = Form(), password: str = Form(), likes: str = Form(), dislikes: str = Form(), inventory: str = Form()):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    db = mongo_client["RecipeDB"]
    users = db.Users
    if await users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User exists")

    pw_bytes = password.encode("utf-8")
    digest = hashlib.sha256(pw_bytes).digest()
    safe = base64.b64encode(digest)
    hashed = pwd.hash(safe)
    await users.insert_one({"username": username, "password": hashed, "likes": likes, "dislikes": dislikes, "inventory": ast.literal_eval(inventory)})
    token = serializer.dumps({"username": username})
    r = JSONResponse({"message": "ok"})
    samesite = "strict" if os.getenv("ENV") == "development" else None
    r.set_cookie("session", token, httponly=True, samesite=samesite, secure=True)
    return r


@auth.post("/login")
async def login(username: str = Form(), password: str = Form()):
    from main import get_mongo_client
    mongo_client = await get_mongo_client()
    db = mongo_client["RecipeDB"]
    users = db.Users
    u = await users.find_one({"username": username})
    pw_bytes = password.encode("utf-8")
    digest = hashlib.sha256(pw_bytes).digest()
    safe = base64.b64encode(digest)
    if not u or not pwd.verify(safe, u["password"]):
        raise HTTPException(status_code=400, detail="invalid creds")

    token = serializer.dumps({"username": username})
    r = JSONResponse({"message": "ok"})
    samesite = "strict" if os.getenv("ENV") == "development" else None
    r.set_cookie("session", token, httponly=True, samesite=samesite, secure= True)
    return r


async def current_user(request: Request):
    c = request.cookies.get("session")
    if not c:
        raise HTTPException(status_code=401, detail="not logged in")
    try:
        d = serializer.loads(c)
        return d["username"]
    except Exception:
        raise HTTPException(status_code=401, detail="bad session")

@auth.get("/check")
async def check(request: Request):
    result = await current_user(request=request)
    if isinstance(result,str):
        return {
            "message" : "ok"
        }



@auth.post("/logout")
async def logout():
    r = JSONResponse({"message": "ok"})
    r.delete_cookie("session")
    return r
