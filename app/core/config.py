import os
from typing import List  # このインポートを追加
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# .envファイルを読み込む
load_dotenv()

# デバッグ出力
print("環境変数の値：")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {'[設定済み]' if os.getenv('DB_PASSWORD') else '[未設定]'}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")

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
    
    # CORS設定
    CORS_ORIGINS_STR: str = Field(default="http://localhost:3000")
    
    # 開発環境フラグ
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
    # プロパティとしてCORS_ORIGINSを実装
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]
    
    # SQLAlchemy接続文字列もプロパティとして実装
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# 設定のインスタンスを作成
settings = Settings()

# デバッグ出力
print("Settings インスタンスの値：")
print(f"SQLALCHEMY_DATABASE_URL: {settings.SQLALCHEMY_DATABASE_URL}")