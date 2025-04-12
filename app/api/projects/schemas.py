from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, description="プロジェクトのタイトル")
    description: Optional[str] = Field(None, description="プロジェクトの詳細説明")
    summary: Optional[str] = Field(None, description="プロジェクトの概要")
    category_id: Optional[int] = Field(None, description="プロジェクトのカテゴリーID")  # 追加: カテゴリーIDフィールド

class ProjectCreate(ProjectBase):
    creator_user_id: int

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None)
    summary: Optional[str] = Field(None)
    category_id: Optional[int] = Field(None, description="プロジェクトのカテゴリーID")  # 追加: カテゴリーIDフィールド

class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True

# 追加: カテゴリー作成用スキーマ
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, description="カテゴリー名")

class ProjectResponse(BaseModel):
    project_id: int
    title: str
    summary: Optional[str]
    description: Optional[str]
    creator_user_id: int
    creator_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    likes: int = 0
    comments: int = 0
    is_favorite: bool = False
    category_id: Optional[int] = None  # 追加: カテゴリーIDフィールド
    category: Optional[CategoryResponse] = None  # 追加: カテゴリー情報

    class Config:
        orm_mode = True

class ProjectListResponse(BaseModel):
    new_projects: List[ProjectResponse]
    favorite_projects: List[ProjectResponse]
    total_projects: int

class UserProjectFavoriteCreate(BaseModel):
    user_id: int
    project_id: int

class RankingUser(BaseModel):
    name: str
    points: int
    rank: int