from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.api.users.models import User
from app.api.users.schemas import TokenData  # 追加したインポート文

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    現在のユーザーを取得する依存関係
    
    :param token: アクセストークン
    :param db: データベースセッション
    :return: 現在のユーザー
    :raises: 認証エラーの場合はHTTPException
    """
    # 開発環境では認証をスキップ
    if settings.DEBUG:
        # デフォルトユーザーを返す（ID=1のユーザーを想定）
        default_user = db.query(User).filter(User.user_id == 1).first()
        if default_user:
            return default_user
        
        # デフォルトユーザーが存在しない場合はエラー
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="開発環境用のデフォルトユーザー（ID=1）が見つかりません。データベースにユーザーを作成してください。",
        )
    
    # 本番環境の通常の認証処理
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    try:
        # JWTトークンからペイロードを取得
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
            
        # 文字列として受け取った場合は整数に変換
        if isinstance(user_id, str):
            user_id = int(user_id)
            
        token_data = TokenData(user_id=user_id)
    except (JWTError, ValueError):
        # JWTエラーまたは整数変換エラー
        raise credentials_exception
    
    # ユーザーIDからユーザーを検索
    user = db.query(User).filter(User.user_id == token_data.user_id).first()
    
    if user is None:
        raise credentials_exception
    
    return user