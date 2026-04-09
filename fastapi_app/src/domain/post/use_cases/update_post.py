from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.posts import PostUpdate, Post as PostSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class UpdatePost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_id: int, post_data: PostUpdate) -> PostSchema:
        try:
            with self._database.session() as session:
                existing = self._repo.get_by_id(session, post_id)
                if not existing:
                    raise NotFoundError(
                        entity_name="Пост",
                        field="id",
                        value=str(post_id)
                    )
                
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
                
                update_data = post_data.model_dump(exclude_unset=True)
                updated = self._repo.update(session, post_id, **update_data)
                
            return PostSchema.model_validate(updated)
        
        except NotFoundError:
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