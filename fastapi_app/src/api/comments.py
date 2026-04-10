from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import (
    comments_by_post,
    create_comment,
    update_comment,
    delete_comment,
    get_current_user,
    get_current_superuser
)
from src.domain.comment.use_cases.get_comments_by_post import GetCommentsByPost
from src.domain.comment.use_cases.create_comment import CreateComment
from src.domain.comment.use_cases.update_comment import UpdateComment
from src.domain.comment.use_cases.delete_comment import DeleteComment
from src.core.exceptions.domain_exceptions import NotFoundError, DomainError, AuthorizationError
from src.schemas.comment import Comment, CommentCreate, CommentUpdate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/post/{post_id}", response_model=List[Comment])
async def get_post_comments(
    post_id: int,
    use_case: GetCommentsByPost = Depends(comments_by_post)
):
    """Получить комментарии к посту. Доступно всем."""
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
    use_case: CreateComment = Depends(create_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Создать новый комментарий. Автор определяется автоматически из токена."""
    try:
        return await use_case.execute(comment_data, current_user.user_id)
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
    use_case: UpdateComment = Depends(update_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Обновить комментарий. Только автор или суперпользователь."""
    try:
        return await use_case.execute(comment_id, comment_data, current_user.user_id, current_user.is_superuser)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
    use_case: DeleteComment = Depends(delete_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Удалить комментарий. Только автор или суперпользователь."""
    try:
        await use_case.execute(comment_id, current_user.user_id, current_user.is_superuser)
        return None
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": e.message, "details": e.details}
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": e.message, "details": e.details}
        )
    except DomainError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": e.message, "details": e.details}
        )