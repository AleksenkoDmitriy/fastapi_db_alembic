from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import (
    comments_by_post,
    create_comment,
    update_comment,
    delete_comment
)
from src.domain.comment.use_cases.get_comments_by_post import GetCommentsByPost
from src.domain.comment.use_cases.create_comment import CreateComment
from src.domain.comment.use_cases.update_comment import UpdateComment
from src.domain.comment.use_cases.delete_comment import DeleteComment
from src.core.exceptions.domain_exceptions import NotFoundError, DomainError
from src.schemas.comment import Comment, CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/post/{post_id}", response_model=List[Comment])
async def get_post_comments(
    post_id: int,
    use_case: GetCommentsByPost = Depends(comments_by_post)
):
    """Получить комментарии к посту"""
    try:
        return await use_case.execute(post_id)
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


@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateComment = Depends(create_comment)
):
    """Создать новый комментарий"""
    try:
        return await use_case.execute(comment_data)
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
    
@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateComment = Depends(update_comment)
):
    """Обновить комментарий"""
    try:
        return await use_case.execute(comment_id, comment_data)
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

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    use_case: DeleteComment = Depends(delete_comment)
):
    try:
        await use_case.execute(comment_id)
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