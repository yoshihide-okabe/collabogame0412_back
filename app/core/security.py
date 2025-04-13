from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from app.core.config import settings

# 環境変数の読み込み
load_dotenv()

# セキュリティ設定
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

# パスワードハッシュ用のコンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    平文のパスワードとデータベースに保存されたパスワードを検証する
    開発環境ではハッシュ化せずに直接比較
    """
    # 開発環境では単純な文字列比較
    if settings.DEBUG:
        return plain_password == stored_password
    # 本番環境では通常のハッシュ検証
    else:
        return pwd_context.verify(plain_password, stored_password)

def get_password_hash(password: str) -> str:
    """
    パスワードをハッシュ化する
    開発環境では平文のまま返す
    """
    # 開発環境ではハッシュ化せずにそのまま返す
    if settings.DEBUG:
        return password
    # 本番環境では通常のハッシュ化
    else:
        return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    # 有効期限の設定
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # トークンをエンコード
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt

def decode_token(token: str):
    """
    JWTトークンをデコードする
    
    :param token: デコードするトークン
    :return: デコードされたペイロード
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None