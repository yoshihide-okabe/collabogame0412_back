from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.config import settings
from ..api.auth.models import User  # 絶対インポートを相対インポートに変更

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーを取得する依存関係
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報が無効です",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # JWTトークンからペイロードを取得
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # ユーザーIDからユーザーを検索
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    
    if user is None:
        raise credentials_exception
    
    return user

def get_optional_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    現在のユーザーを取得する依存関係（トークンがなくてもOK）
    """
    if not token:
        return None
        
    try:
        # JWTトークンからペイロードを取得
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
    except JWTError:
        return None
    
    # ユーザーIDからユーザーを検索
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    
    return user