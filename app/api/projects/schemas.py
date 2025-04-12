from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, description="プロジェクトのタイトル")
    description: Optional[str] = Field(None, description="プロジェクトの詳細説明")
    summary: Optional[str] = Field(None, description="プロジェクトの概要")

class ProjectCreate(ProjectBase):
    creator_user_id: int

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None)
    summary: Optional[str] = Field(None)

class CategoryResponse(BaseModel):
    category_id: int
    name: str

    class Config:
        orm_mode = True

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