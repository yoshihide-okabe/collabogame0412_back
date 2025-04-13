from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class TroubleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="お困りごとのタイトル")
    description: str = Field(..., min_length=10, max_length=1000, description="お困りごとの詳細説明")
    category_id: int = Field(..., description="お困りごとのカテゴリーID")  # 型を修正
    status: Optional[str] = Field(None, description="お困りごとの状態 ('未解決' または '解決')")

class TroubleCreate(TroubleBase):
    project_id: int = Field(..., description="関連するプロジェクトID")

class TroubleUpdate(TroubleBase):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category_id: Optional[int] = Field(None)
    status: Optional[str] = Field(None)

class TroubleResponse(TroubleBase):
    id: int
    project_id: int
    project_title: str
    creator_user_id: int  # フィールド名を統一
    creator_name: str     # フィールド名を統一
    created_at: datetime
    comments: int = 0

    class Config:
        orm_mode = True

class TroubleDetailResponse(TroubleResponse):
    # メッセージ関連の情報を追加する場合
    # messages: List[MessageResponse] = []
    pass

class TroublesListResponse(BaseModel):
    troubles: List[TroubleResponse]
    total: int
    
class TroubleCategoryResponse(BaseModel):
    category_id: int
    name: str
    
    class Config:
        orm_mode = True
        
# 追加: カテゴリー作成用スキーマ
class TroubleCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, description="カテゴリー名")