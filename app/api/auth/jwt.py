from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.security import verify_password, SECRET_KEY, ALGORITHM
from app.core.config import settings

from app.core.database import get_db
from app.api.users.models import User
from app.api.users.schemas import TokenData

# OAuth2のパスワードベアラースキーマを定義
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    ユーザー名とパスワードでユーザーを認証する
    
    :param db: データベースセッション
    :param username: ユーザー名
    :param password: パスワード
    :return: 認証されたユーザー、または認証失敗の場合はNone
    """
    user = db.query(User).filter(User.name == username).first()
    if not user or not verify_password(password, user.password): #hashed_passwordをpasswordに変更
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    アクセストークンを生成する
    
    :param data: トークンに含めるデータ
    :param expires_delta: トークンの有効期限
    :return: JWTトークン
    """
    to_encode = data.copy()
    
    # 有効期限の設定
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # トークンをエンコード
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt