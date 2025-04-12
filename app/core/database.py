from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# データベースエンジンの作成
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.DEBUG  # デバッグモードの場合、SQLクエリをコンソールに表示
)

# セッションファクトリの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

def get_db():
    """
    依存性注入用のデータベースセッション取得関数
    FastAPIのDependsで使用する
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()