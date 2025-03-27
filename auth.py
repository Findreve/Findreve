from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import json
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from nicegui import ui, app

# 得到这样的字符串 / to get a string like this run: 
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 模拟存储的用户名和密码（实际应用中应该从数据库或其他安全存储中获取）
# Emulate the username and password stored in the database (in real applications, you should get them from a database or other secure storage)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

# FastAPI 鉴权模型
# FastAPI authentication model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# FastAPI 登录路由 / FastAPI login route
@app.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# FastAPI 获取个人信息路由 / FastAPI get personal information route
@app.get("/api/profile")
async def profile(
    current_user: Annotated[User, Depends(get_current_active_user)],
                            ):
    """
    需要鉴权的路由示例
    :param credentials: FastAPI 提供的用于解析HTTP Basic Auth头部的对象
    :return: 成功时返回鉴权成功的消息，否则返回鉴权失败的HTTP错误
    """
    return current_user

# NiceGUI 获取个人信息路由 / NiceGUI get personal information route
@ui.page("/profile")
async def profile():
    """
    需要鉴权的路由示例
    :param credentials: FastAPI 提供的用于解析HTTP Basic Auth头部的对象
    :return: 成功时返回鉴权成功的消息，否则返回鉴权失败的HTTP错误
    """
    ui.add_head_html("""
                    <script>
                     async function getProfile() {
                        const accessToken = localStorage.getItem('access_token');
                        
                        if (!accessToken) {
                            return {'status': 'failed', 'detail': 'Access token not found'};
                        }

                        const url = '/api/profile';

                        try {
                            const response = await fetch(url, {
                                method: 'GET',
                                headers: {
                                    'Authorization': `Bearer ${accessToken}`,
                                },
                            });

                            if (!response.ok) {
                                throw new Error('Failed to fetch profile');
                            }

                            const profile = await response.json();

                            return {'status': 'success', 'profile': profile};

                        } catch (error) {
                            return {'status': 'failed', 'detail': error.message};
                        }
                    }
                    
                    function logout() {
                        localStorage.removeItem('access_token');
                        window.location.reload();
                    }
                    </script>
                    """)
    await ui.context.client.connected()
    result = await ui.run_javascript("getProfile()")
    if result['status'] == 'success':
        ui.label(f"Profile: {json.dumps(result['profile'])}")
        ui.button("Logout", on_click=lambda: ui.run_javascript("logout()"))
    else:
        ui.label("Failed to fetch profile. Please login first.")
        ui.button("Login", on_click=lambda: ui.navigate.to("/login"))
    

# 登录界面路由 / Login page route
@ui.page("/login")
async def login_page():
    """
    登录界面路由示例
    :return: 一个登录页面
    """
    ui.add_head_html("""
                     <script>
                     async function login(username, password) {
                        const url = '/api/token';
                        const data = new URLSearchParams();
                        data.append('username', username);
                        data.append('password', password);

                        try {
                            const response = await fetch(url, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                },
                                body: data,
                            });

                            if (!response.ok) {
                                throw new Error('Invalid username or password');
                            }

                            const result = await response.json();

                            // 处理登录成功后的数据，返回access_token
                            localStorage.setItem('access_token', result.access_token);

                            return {'status': 'success'};

                        } catch (error) {
                            return {'status': 'failed', 'detail': error.message};
                        }
                    }
                    </script>
                     """)
    
    async def try_login():
        username = usrname.value
        password = pwd.value
        
        if username and password:
            result = await ui.run_javascript(f"login('{username}', '{password}')")
            if result['status'] == 'success':
                ui.navigate.to("/profile")
            else:
                ui.notify("Login failed. Please try again.", type="negative")
    usrname = ui.input("username")
    pwd = ui.input("password", password=True)
    ui.button("Login", on_click=try_login)

# 公开路由 / Public page route
@ui.page("/")
async def public_data():
    """
    公开路由示例
    :return: 一个公开的消息，无需鉴权
    """
    ui.label("This is a public page.")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(uvicorn_logging_level='debug')