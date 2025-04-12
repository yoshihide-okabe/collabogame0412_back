from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 相対インポートに変更
from ...core.database import Base

class ProjectCategory(Base):
    __tablename__ = "project_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)

class CoCreationProject(Base):
    __tablename__ = "co_creation_projects"

    project_id = Column(Integer, primary_key=True, index=True)
    creator_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    category_id = Column(Integer, ForeignKey("project_categories.category_id"), nullable=True)  # 追加: カテゴリーIDの外部キー
    title = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    
    # リレーションシップ
    creator = relationship("User", back_populates="projects")
    category = relationship("ProjectCategory", back_populates="projects")  # 追加: カテゴリーとのリレーションシップ
    troubles = relationship("Trouble", back_populates="project")
    favorites = relationship("UserProjectFavorite", back_populates="project")
    participants = relationship("UserProjectParticipation", back_populates="project")

class UserProjectFavorite(Base):
    __tablename__ = "user_project_favorites"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("co_creation_projects.project_id"), primary_key=True)
    
    # リレーションシップ
    user = relationship("User", back_populates="favorite_projects")
    project = relationship("CoCreationProject", back_populates="favorites")

class UserProjectParticipation(Base):
    __tablename__ = "user_project_participation"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("co_creation_projects.project_id"), primary_key=True)
    selected_at = Column(DateTime, nullable=False)
    
    # リレーションシップ
    user = relationship("User", back_populates="participating_projects")
    project = relationship("CoCreationProject", back_populates="participants")