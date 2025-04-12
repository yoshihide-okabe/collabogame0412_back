
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.api.auth.models import User
from app.api.projects.models import CoCreationProject, UserProjectFavorite, ProjectCategory
from app.api.projects.schemas import (
    ProjectResponse, 
    ProjectListResponse, 
    ProjectCreate, 
    ProjectUpdate,
    CategoryResponse,
    RankingUser
)

router = APIRouter()

@router.get("/", response_model=ProjectListResponse)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.user_id
    
    # 新着プロジェクト
    new_projects = (
        db.query(CoCreationProject)
        .order_by(CoCreationProject.created_at.desc())
        .limit(8)
        .all()
    )

    # お気に入りプロジェクト
    favorite_projects = (
        db.query(CoCreationProject)
        .join(UserProjectFavorite)
        .filter(UserProjectFavorite.user_id == user_id)
        .order_by(CoCreationProject.created_at.desc())
        .limit(8)
        .all()
    )

    # プロジェクト総数
    total_projects = db.query(CoCreationProject).count()

    # プロジェクトをレスポンススキーマに変換
    def convert_project(project):
        # ダミーのいいね数とコメント数
        likes = 24  # TODO: 実際のロジックに置き換える
        comments = 8  # TODO: 実際のロジックに置き換える
        
        # お気に入り判定
        is_favorite = db.query(UserProjectFavorite).filter(
            UserProjectFavorite.user_id == user_id,
            UserProjectFavorite.project_id == project.project_id
        ).first() is not None

        # プロジェクト作成者の情報取得
        creator = db.query(User).filter(User.user_id == project.creator_user_id).first()

        return ProjectResponse(
            project_id=project.project_id,
            title=project.title,
            summary=project.summary if hasattr(project, 'summary') else None,
            description=project.description,
            creator_user_id=project.creator_user_id,
            creator_name=creator.name if creator else "不明",
            created_at=project.created_at,
            updated_at=project.updated_at if hasattr(project, 'updated_at') else None,
            likes=likes,
            comments=comments,
            is_favorite=is_favorite
        )

    return ProjectListResponse(
        new_projects=[convert_project(p) for p in new_projects],
        favorite_projects=[convert_project(p) for p in favorite_projects],
        total_projects=total_projects
    )

@router.get("/categories", response_model=List[CategoryResponse])
def get_project_categories(db: Session = Depends(get_db)):
    # データベースからカテゴリを取得
    categories = db.query(ProjectCategory).all()
    
    # カテゴリがない場合は初期データを挿入
    if not categories:
        default_categories = [
            "テクノロジー", "デザイン", "マーケティング", "ビジネス", 
            "教育", "コミュニティ", "医療", "環境"
        ]
        
        for name in default_categories:
            category = ProjectCategory(name=name)
            db.add(category)
        
        db.commit()
        categories = db.query(ProjectCategory).all()
    
    return [
        CategoryResponse(
            category_id=category.category_id,
            name=category.name
        ) for category in categories
    ]

@router.get("/ranking", response_model=List[RankingUser])
def get_activity_ranking(db: Session = Depends(get_db)):
    # TODO: 実際のポイント計算ロジックに置き換える
    # 現時点では、ダミーデータを返す
    ranking_data = [
        RankingUser(name="キツネ", points=1250, rank=1),
        RankingUser(name="パンダ", points=980, rank=2),
        RankingUser(name="ウサギ", points=875, rank=3)
    ]
    return ranking_data

@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # プロジェクト作成のバリデーション
    if not project.title or not project.description:
        raise HTTPException(status_code=400, detail="必須項目を入力してください")

    # 自分以外のユーザーIDでプロジェクトを作成できないようにする
    if project.creator_user_id != current_user.user_id:
        raise HTTPException(
            status_code=403, 
            detail="自分以外のユーザーIDでプロジェクトを作成することはできません"
        )

    # プロジェクトを作成
    new_project = CoCreationProject(
        title=project.title,
        summary=project.summary,
        description=project.description,
        creator_user_id=current_user.user_id,
        created_at=datetime.now()
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "message": "プロジェクトを登録しました", 
        "project_id": new_project.project_id
    }

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    # プロジェクトの詳細を取得
    project = db.query(CoCreationProject).filter(CoCreationProject.project_id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="プロジェクトが見つかりません")
    
    # TODO: いいね数とコメント数の実装
    likes = 24  # 仮の値
    comments = 8  # 仮の値
    
    # お気に入り判定
    is_favorite = False
    if current_user:
        is_favorite = db.query(UserProjectFavorite).filter(
            UserProjectFavorite.user_id == current_user.user_id,
            UserProjectFavorite.project_id == project_id
        ).first() is not None
    
    # プロジェクト作成者の情報取得
    creator = db.query(User).filter(User.user_id == project.creator_user_id).first()
    
    return ProjectResponse(
        project_id=project.project_id,
        title=project.title,
        summary=project.summary,
        description=project.description,
        creator_user_id=project.creator_user_id,
        creator_name=creator.name if creator else "不明",
        created_at=project.created_at,
        updated_at=project.updated_at,
        likes=likes,
        comments=comments,
        is_favorite=is_favorite
    )

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """プロジェクトを更新"""
    db_project = db.query(CoCreationProject).filter(CoCreationProject.project_id == project_id).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="プロジェクトが見つかりません"
        )
    
    # プロジェクトの所有者のみが更新可能
    if db_project.creator_user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="このプロジェクトを更新する権限がありません"
        )
    
    # 更新データを適用
    update_data = project_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_project, key, value)
    
    # 更新日時を設定
    db_project.updated_at = datetime.now()
    
    db.commit()
    db.refresh(db_project)
    
    # プロジェクト作成者の情報取得
    creator = db.query(User).filter(User.user_id == db_project.creator_user_id).first()
    
    return ProjectResponse(
        project_id=db_project.project_id,
        title=db_project.title,
        summary=db_project.summary,
        description=db_project.description,
        creator_user_id=db_project.creator_user_id,
        creator_name=creator.name if creator else "不明",
        created_at=db_project.created_at,
        updated_at=db_project.updated_at,
        likes=24,  # 仮の値
        comments=8,  # 仮の値
        is_favorite=False  # 更新後のお気に入り状態は別途取得必要
    )