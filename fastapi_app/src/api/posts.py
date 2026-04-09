from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from src.api.depends import (
    posts,
    post,
    create_post,
    update_post,
    delete_post
)
from src.domain.post.use_cases.get_posts import GetPosts
from src.domain.post.use_cases.get_post import GetPost
from src.domain.post.use_cases.create_post import CreatePost
from src.domain.post.use_cases.update_post import UpdatePost
from src.domain.post.use_cases.delete_post import DeletePost
from src.core.exceptions.domain_exceptions import NotFoundError, DomainError
from src.schemas.posts import Post, PostCreate, PostUpdate, PostListResponse

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostListResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    use_case: GetPosts = Depends(posts)
):
    try:
        return await use_case.execute(skip=skip, limit=limit, category_id=category_id)
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    use_case: GetPost = Depends(post)
):
    try:
        post = await use_case.execute(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пост не найден"
            )
        return post
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    use_case: CreatePost = Depends(create_post)
):
    try:
        return await use_case.execute(post_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )
    
@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    use_case: UpdatePost = Depends(update_post)
):
    try:
        return await use_case.execute(post_id, post_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    use_case: DeletePost = Depends(delete_post)
):
    try:
        await use_case.execute(post_id)
        return None
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )