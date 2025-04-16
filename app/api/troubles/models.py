from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class TroubleCategory(Base):
    __tablename__ = "trouble_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    
    # リレーションシップ
    troubles = relationship("Trouble", back_populates="category")

class Trouble(Base):
    __tablename__ = "troubles"

    trouble_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("co_creation_projects.project_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("trouble_categories.category_id"), nullable=False)
    creator_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # 名前を統一: author_id → creator_user_id
    description = Column(Text, nullable=False)   
    created_at = Column(DateTime(timezone=True), server_default=func.now())
#    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, default="未解決")
    
    # リレーションシップ
    project = relationship("CoCreationProject", back_populates="troubles")
    author = relationship("User", back_populates="troubles")
    category = relationship("TroubleCategory", back_populates="troubles")  # この行を追加
    # メッセージ機能を実装する場合
    messages = relationship("Message", back_populates="trouble")