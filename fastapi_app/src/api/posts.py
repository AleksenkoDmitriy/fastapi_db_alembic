from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime
from pathlib import Path
import uuid
import shutil
from pydantic import ValidationError as PydanticValidationError

from src.api.depends import (
    posts,
    post,
    create_post,
    update_post,
    delete_post,
    get_current_user
)
from src.domain.post.use_cases.get_posts import GetPosts
from src.domain.post.use_cases.get_post import GetPost
from src.domain.post.use_cases.create_post import CreatePost
from src.domain.post.use_cases.update_post import UpdatePost
from src.domain.post.use_cases.delete_post import DeletePost
from src.schemas.posts import PostCreate, PostUpdate, PostResponse
from src.schemas.auth import TokenData
from src.core.config import settings
from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.models.post import Post as PostModel

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    use_case: GetPosts = Depends(posts)
):
    """Получить список постов. Доступно всем."""
    return await use_case.execute(skip=skip, limit=limit, category_id=category_id)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    use_case: GetPost = Depends(post)
):
    """Получить пост по ID. Доступно всем."""
    return await use_case.execute(post_id)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(...),
    text: str = Form(...),
    pub_date: Optional[str] = Form(None),
    category_id: int = Form(...),
    location_id: int = Form(0),
    is_published: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    use_case: CreatePost = Depends(create_post),
    current_user: TokenData = Depends(get_current_user)
):
    """Создать новый пост с возможностью сразу загрузить картинку."""
    location_id_value = location_id if location_id > 0 else None
    
    pub_date_dt = None
    if pub_date:
        try:
            pub_date_dt = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "Неверный формат даты", "field": "pub_date"}
            )
    
    try:
        post_data = PostCreate(
            title=title.strip(),
            text=text.strip(),
            pub_date=pub_date_dt,
            category_id=category_id,
            location_id=location_id_value,
            is_published=is_published
        )
    except PydanticValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Ошибка валидации данных", "errors": e.errors()}
        )
    
    post = await use_case.execute(post_data, current_user.user_id)
    
    if image and image.filename:
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_ext = Path(image.filename).suffix
        unique_filename = f"{post.id}_{uuid.uuid4().hex}{file_ext}"
        file_path = upload_dir / unique_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/uploads/{unique_filename}"
        
        with database.session() as session:
            session.query(PostModel).filter(PostModel.id == post.id).update({"image": image_url})
            session.commit()
        
        post.image = image_url
    
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    title: Optional[str] = Form(None),
    text: Optional[str] = Form(None),
    pub_date: Optional[str] = Form(None),
    category_id: Optional[int] = Form(None),
    location_id: Optional[int] = Form(None),
    is_published: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    remove_image: bool = Form(False),
    use_case: UpdatePost = Depends(update_post),
    current_user: TokenData = Depends(get_current_user)
):
    """Обновить пост. Только автор или суперпользователь."""
    update_dict = {}
    
    if title is not None:
        if not title.strip() or len(title.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "Заголовок должен содержать минимум 5 символов", "field": "title"}
            )
        update_dict["title"] = title.strip()
    
    if text is not None:
        if not text.strip() or len(text.strip()) < 20:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "Текст должен содержать минимум 20 символов", "field": "text"}
            )
        update_dict["text"] = text.strip()
    
    if pub_date is not None:
        try:
            update_dict["pub_date"] = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "Неверный формат даты", "field": "pub_date"}
            )
    
    if category_id is not None:
        if category_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"message": "ID категории должен быть положительным", "field": "category_id"}
            )
        update_dict["category_id"] = category_id
    
    if location_id is not None:
        update_dict["location_id"] = location_id if location_id > 0 else None
    
    if is_published is not None:
        update_dict["is_published"] = is_published
    
    if image and image.filename:
        if not image.content_type or not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        upload_dir = Path(settings.UPLOAD_DIR)
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_ext = Path(image.filename).suffix
        unique_filename = f"{post_id}_{uuid.uuid4().hex}{file_ext}"
        file_path = upload_dir / unique_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        image_url = f"/uploads/{unique_filename}"
        update_dict["image"] = image_url
        
        with database.session() as session:
            old_post = session.query(PostModel).filter(PostModel.id == post_id).first()
            if old_post and old_post.image:
                old_image_path = Path(settings.UPLOAD_DIR) / Path(old_post.image).name
                if old_image_path.exists():
                    old_image_path.unlink()
    
    elif remove_image:
        update_dict["image"] = None
        with database.session() as session:
            old_post = session.query(PostModel).filter(PostModel.id == post_id).first()
            if old_post and old_post.image:
                old_image_path = Path(settings.UPLOAD_DIR) / Path(old_post.image).name
                if old_image_path.exists():
                    old_image_path.unlink()
    
    if update_dict:
        post_update = PostUpdate(**update_dict)
        return await use_case.execute(post_id, post_update, current_user.user_id, current_user.is_superuser)
    
    return await GetPost().execute(post_id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case: DeletePost = Depends(delete_post),
    current_user: TokenData = Depends(get_current_user)
):
    """Удалить пост. Только автор или суперпользователь."""
    await use_case.execute(post_id, current_user.user_id, current_user.is_superuser)
    return None