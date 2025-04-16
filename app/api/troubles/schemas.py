from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

    
class TroubleCreate(BaseModel):
    project_id: int = Field(..., description="関連するプロジェクトID")
    category_id: int = Field(..., description="お困りごとのカテゴリーID")
    description: str = Field(..., min_length=10, max_length=1000, description="お困りごとの詳細説明")
    status: Optional[str] = Field("未解決", description="お困りごとの状態 ('未解決' または '解決')")

    
class TroubleUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    category_id: Optional[int] = Field(None)
    status: Optional[str] = Field(None)    

class TroubleResponse(BaseModel):
    trouble_id: int
    description: str
    category_id: int
    project_id: int
    project_title: str  # router.pyで使用されているフィールド
    creator_user_id: int
    creator_name: str
    created_at: datetime
    status: str
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