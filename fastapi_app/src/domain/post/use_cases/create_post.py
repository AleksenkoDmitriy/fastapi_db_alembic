from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.locations import LocationRepository
from src.schemas.posts import PostCreate, Post as PostSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class CreatePost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._location_repo = LocationRepository()

    async def execute(self, post_data: PostCreate, author_id: int) -> PostSchema:
        try:
            with self._database.session() as session:
                category = self._category_repo.get_by_id(session, post_data.category_id)
                if not category:
                    raise NotFoundError(
                        entity_name="Категория",
                        field="id",
                        value=str(post_data.category_id)
                    )
                
                if post_data.location_id:
                    location = self._location_repo.get_by_id(session, post_data.location_id)
                    if not location:
                        raise NotFoundError(
                            entity_name="Локация",
                            field="id",
                            value=str(post_data.location_id)
                        )
                
                post_dict = post_data.model_dump()
                post_dict["author_id"] = author_id
                
                post = self._repo.create(session, **post_dict)
                
            return PostSchema.model_validate(post)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании поста '{post_data.title}'",
                details={"title": post_data.title, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании поста '{post_data.title}'",
                details={"title": post_data.title, "error": str(e)}
            )