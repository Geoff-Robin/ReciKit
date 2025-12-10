from fastapi import APIRouter, Form, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeSerializer
from passlib.context import CryptContext
import os

auth = APIRouter()

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeSerializer(os.getenv("SECRET_KEY"))


@auth.post("/signup")
async def signup(username: str = Form(), password: str = Form(), likes: str = Form(), dislikes: str = Form()):
    global mongo_client
    db = mongo_client["RecipeDB"]
    users = db.Users
    if await users.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User exists")

    hashed = pwd.hash(password)
    await users.insert_one({"username": username, "password": hashed, "likes": likes, "dislikes": dislikes})
    token = serializer.dumps({"username": username})
    r = JSONResponse({"message": "ok"})
    r.set_cookie("session", token, httponly=True, samesite="strict")
    return r


@auth.post("/login")
async def login(username: str = Form(), password: str = Form()):
    global mongo_client
    db = mongo_client["RecipeDB"]
    users = db.Users
    u = await users.find_one({"username": username})
    if not u or not pwd.verify(password, u["password"]):
        raise HTTPException(status_code=400, detail="invalid creds")

    token = serializer.dumps({"username": username})
    r = JSONResponse({"message": "ok"})
    r.set_cookie("session", token, httponly=True, samesite="strict")
    return r


def current_user(request: Request):
    c = request.cookies.get("session")
    if not c:
        raise HTTPException(status_code=401, detail="not logged in")
    try:
        d = serializer.loads(c)
        return d["username"]
    except Exception:
        raise HTTPException(status_code=401, detail="bad session")


@auth.get("/dashboard")
async def dashboard(user: str = Depends(current_user)):
    return {"message": user}


@auth.post("/logout")
async def logout():
    r = JSONResponse({"message": "ok"})
    r.delete_cookie("session")
    return r
