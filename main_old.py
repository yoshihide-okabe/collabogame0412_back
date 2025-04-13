from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uvicorn
import sys
import os
from datetime import timedelta

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 認証関連のインポート
from app.core.database import get_db
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.auth.jwt import authenticate_user, create_access_token
from app.api.users.schemas import Token

# APIルーターのインポート
from app.api.troubles.router import router as troubles_router
from app.api.projects.router import router as projects_router
from app.api.users.router import router as users_router
from app.api.messages.router import router as messages_router
from app.api.auth.router import router as auth_router

app = FastAPI(
    title="CollaboGames Backend API",
    description="コラボゲームズのバックエンドAPIサービス",
    version="0.1.0"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # フロントエンドのオリジンに置き換えてください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの追加
app.include_router(troubles_router, prefix="/api/troubles", tags=["troubles"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(messages_router, prefix="/api/messages", tags=["messages"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# ルートレベルに /token エンドポイントを追加
@app.post("/token", response_model=Token)
def root_token_endpoint(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    OAuth2互換のトークンログインエンドポイント（ルートレベル）
    """
    # ユーザーを認証
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが無効です",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # アクセストークンを生成
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.name
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to CollaboGames Backend API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)