import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# .envファイルを読み込む
load_dotenv()

class Settings(BaseSettings):
    # サーバー設定
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # アプリケーション設定
    PROJECT_NAME: str = "COLLABOAGAMES0406 API"
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
    
    # データベース設定
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "collabo_db")
    
    # SQLAlchemy接続文字列
    SQLALCHEMY_DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # CORS設定
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # 開発環境フラグ
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

# 設定のインスタンスを作成
settings = Settings()