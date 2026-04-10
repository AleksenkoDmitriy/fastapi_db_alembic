from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.database import database

# Category Use Cases
from src.domain.category.use_cases.get_categories import GetCategories
from src.domain.category.use_cases.get_category import GetCategory
from src.domain.category.use_cases.get_category_by_slug import GetCategoryBySlug
from src.domain.category.use_cases.create_category import CreateCategory
from src.domain.category.use_cases.update_category import UpdateCategory
from src.domain.category.use_cases.delete_category import DeleteCategory

# Location Use Cases
from src.domain.location.use_cases.get_locations import GetLocations
from src.domain.location.use_cases.get_location import GetLocation
from src.domain.location.use_cases.create_location import CreateLocation
from src.domain.location.use_cases.update_location import UpdateLocation
from src.domain.location.use_cases.delete_location import DeleteLocation

# Post Use Cases
from src.domain.post.use_cases.get_posts import GetPosts
from src.domain.post.use_cases.get_post import GetPost
from src.domain.post.use_cases.create_post import CreatePost
from src.domain.post.use_cases.update_post import UpdatePost
from src.domain.post.use_cases.delete_post import DeletePost

# Comment Use Cases
from src.domain.comment.use_cases.get_comments_by_post import GetCommentsByPost
from src.domain.comment.use_cases.create_comment import CreateComment
from src.domain.comment.use_cases.update_comment import UpdateComment
from src.domain.comment.use_cases.delete_comment import DeleteComment

# User Use Cases
from src.domain.user.use_cases.get_users import GetUsers
from src.domain.user.use_cases.get_user_by_id import GetUserById
from src.domain.user.use_cases.get_user_by_login import GetUserByLogin
from src.domain.user.use_cases.create_user import CreateUser
from src.domain.user.use_cases.update_user import UpdateUser
from src.domain.user.use_cases.delete_user import DeleteUser

# Auth Use Cases
from src.domain.auth.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.auth.use_cases.create_access_token import CreateAccessTokenUseCase

# Auth Dependencies (для защиты роутов)
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from src.resources.auth import decode_token
from src.core.exceptions.auth_exceptions import CredentialsException, TokenExpiredException, InvalidTokenException
from src.schemas.auth import TokenData

security = HTTPBearer()


def get_db():
    with database.session() as session:
        yield session


# Category
def categories() -> GetCategories:
    return GetCategories()

def category() -> GetCategory:
    return GetCategory()

def category_by_slug() -> GetCategoryBySlug:
    return GetCategoryBySlug()

def create_category() -> CreateCategory:
    return CreateCategory()

def update_category() -> UpdateCategory:
    return UpdateCategory()

def delete_category() -> DeleteCategory:
    return DeleteCategory()


# Location
def locations() -> GetLocations:
    return GetLocations()

def location() -> GetLocation:
    return GetLocation()

def create_location() -> CreateLocation:
    return CreateLocation()

def update_location() -> UpdateLocation:
    return UpdateLocation()

def delete_location() -> DeleteLocation:
    return DeleteLocation()


# Post
def posts() -> GetPosts:
    return GetPosts()

def post() -> GetPost:
    return GetPost()

def create_post() -> CreatePost:
    return CreatePost()

def update_post() -> UpdatePost:
    return UpdatePost()

def delete_post() -> DeletePost:
    return DeletePost()


# Comment
def comments_by_post() -> GetCommentsByPost:
    return GetCommentsByPost()

def create_comment() -> CreateComment:
    return CreateComment()

def update_comment() -> UpdateComment:
    return UpdateComment()

def delete_comment() -> DeleteComment:
    return DeleteComment()


# User
def users() -> GetUsers:
    return GetUsers()

def user_by_id() -> GetUserById:
    return GetUserById()

def user_by_login() -> GetUserByLogin:
    return GetUserByLogin()

def create_user() -> CreateUser:
    return CreateUser()

def update_user() -> UpdateUser:
    return UpdateUser()

def delete_user() -> DeleteUser:
    return DeleteUser()


# Auth Use Cases
def authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase()

def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


# Auth Dependencies для защиты роутов
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    try:
        token = credentials.credentials
        payload = decode_token(token)
        
        user_id = payload.get("sub")
        username = payload.get("username")
        
        if user_id is None or username is None:
            raise CredentialsException()
        
        return TokenData(
            user_id=int(user_id),
            username=username,
            is_superuser=payload.get("is_superuser", False),
            is_staff=payload.get("is_staff", False)
        )
    
    except JWTError as e:
        if "expired" in str(e).lower():
            raise TokenExpiredException()
        raise InvalidTokenException()


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    return current_user


async def get_current_superuser(
    current_user: TokenData = Depends(get_current_active_user)
) -> TokenData:
    if not current_user.is_superuser:
        from src.core.exceptions.auth_exceptions import InsufficientPermissionsException
        raise InsufficientPermissionsException("Требуются права суперпользователя")
    return current_user


async def get_current_staff_user(
    current_user: TokenData = Depends(get_current_active_user)
) -> TokenData:
    if not current_user.is_staff and not current_user.is_superuser:
        from src.core.exceptions.auth_exceptions import InsufficientPermissionsException
        raise InsufficientPermissionsException("Недостаточно прав для выполнения операции")
    return current_user