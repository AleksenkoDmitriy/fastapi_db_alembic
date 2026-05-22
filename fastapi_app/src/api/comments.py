from fastapi import APIRouter, Depends
from typing import List
from src.api.depends import (
    comments_by_post,
    create_comment,
    update_comment,
    delete_comment,
    get_current_user
)
from src.domain.comment.use_cases.get_comments_by_post import GetCommentsByPost
from src.domain.comment.use_cases.create_comment import CreateComment
from src.domain.comment.use_cases.update_comment import UpdateComment
from src.domain.comment.use_cases.delete_comment import DeleteComment
from src.schemas.comment import Comment, CommentCreate, CommentUpdate
from src.schemas.auth import TokenData

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/post/{post_id}", response_model=List[Comment])
async def get_post_comments(
    post_id: int,
    use_case: GetCommentsByPost = Depends(comments_by_post)
):
    """Получить комментарии к посту. Доступно всем."""
    return await use_case.execute(post_id)


@router.post("/", response_model=Comment, status_code=201)
async def create_comment(
    comment_data: CommentCreate,
    use_case: CreateComment = Depends(create_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Создать новый комментарий. Автор определяется автоматически из токена."""
    return await use_case.execute(comment_data, current_user.user_id)


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    use_case: UpdateComment = Depends(update_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Обновить комментарий. Только автор."""
    return await use_case.execute(comment_id, comment_data, current_user.user_id)


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    use_case: DeleteComment = Depends(delete_comment),
    current_user: TokenData = Depends(get_current_user)
):
    """Удалить комментарий. Только автор или суперпользователь."""
    await use_case.execute(comment_id, current_user.user_id, current_user.is_superuser)
    return None