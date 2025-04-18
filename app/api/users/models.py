from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base  # 集約したBaseをインポート

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    #hashed_password = Column(String, nullable=False)
    password = Column(String, nullable=False) 
    category_id = Column(Integer, ForeignKey("project_categories.category_id"))
    num_answer = Column(Integer) 
    point_total = Column(Integer, default=0) 
    #created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime, nullable=False)  
    
    # リレーションシップ - 文字列で参照する
    projects = relationship("CoCreationProject", back_populates="creator")  # ← 修正
    favorite_projects = relationship("UserProjectFavorite", back_populates="user")  # ← 修正
    participating_projects = relationship("UserProjectParticipation", back_populates="user")  # ← 追加
    messages = relationship("Message", back_populates="user")
    troubles = relationship("Trouble", back_populates="author")
    
    def get_categories_list(self):
        """カテゴリー文字列をリストに変換"""
        if not self.categories:
            return []
        return [cat.strip() for cat in self.categories.split(",")]
    
    def set_categories_list(self, categories_list):
        """カテゴリーリストを文字列に変換"""
        if not categories_list:
            self.categories = ""
        else:
            self.categories = ",".join(categories_list)