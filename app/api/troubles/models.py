from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class Trouble(Base):
    __tablename__ = "troubles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, nullable=False)  # または適切な外部キーを設定
    
    
    project_id = Column(Integer, ForeignKey("co_creation_projects.project_id"), nullable=False)
    
    creator_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 名前を統一: author_id → creator_user_id
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, default="未解決")
    
    # リレーションシップ
    project = relationship("CoCreationProject", back_populates="troubles")
    author = relationship("User", back_populates="troubles")
    # メッセージ機能を実装する場合
    messages = relationship("Message", back_populates="trouble")