from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.locations import LocationRepository
from src.schemas.posts import PostUpdate, Post as PostSchema
from src.core.exceptions import DomainError, NotFoundError, AuthorizationError, DatabaseError
from src.infrastructure.postgres.models.users import User
from src.infrastructure.postgres.models.category import Category
from src.infrastructure.postgres.models.location import Location
from src.infrastructure.postgres.models.post import Post as PostModel


class UpdatePost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_id: int, post_data: PostUpdate, current_user_id: int, is_superuser: bool) -> PostSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, post_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(post_id)
                    )
                
                if existing.author_id != current_user_id and not is_superuser:
                    raise AuthorizationError("Вы можете редактировать только свои посты")
                
                if post_data.category_id is not None:
                    category = self._category_repo.get_by_id(session, post_data.category_id)
                    if not category:
                        raise NotFoundError(
                            entity_name="Категория",
                            field="id",
                            value=str(post_data.category_id)
                        )
                
                if post_data.location_id is not None:
                    location = self._location_repo.get_by_id(session, post_data.location_id)
                    if not location:
                        raise NotFoundError(
                            entity_name="Локация",
                            field="id",
                            value=str(post_data.location_id)
                        )
                
                update_data = post_data.model_dump(exclude_unset=False)
                
                if update_data.get("image") is None and "image" in update_data:
                    update_data["image"] = None
                
                if update_data:
                    self._repo.update(session, post_id, **update_data)
                
                updated_post = session.query(PostModel).filter(PostModel.id == post_id).first()
                
                author = session.get(User, updated_post.author_id)
                category = session.get(Category, updated_post.category_id)
                location = session.get(Location, updated_post.location_id) if updated_post.location_id else None
                
                post_dict = {
                    "id": updated_post.id,
                    "title": updated_post.title,
                    "text": updated_post.text,
                    "pub_date": updated_post.pub_date,
                    "is_published": updated_post.is_published,
                    "created_at": updated_post.created_at,
                    "image": updated_post.image,
                    "author": author,
                    "category": category,
                    "location": location,
                    "author_id": updated_post.author_id,
                    "category_id": updated_post.category_id,
                    "location_id": updated_post.location_id
                }
                
                return PostSchema.model_validate(post_dict)
        
        except (NotFoundError, AuthorizationError):
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при обновлении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при обновлении поста ID={post_id}",
                details={"post_id": post_id, "error": str(e)}
            )