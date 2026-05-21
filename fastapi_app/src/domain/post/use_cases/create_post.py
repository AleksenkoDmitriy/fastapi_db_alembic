from src.infrastructure.postgres.database import database
from src.infrastructure.postgres.repositories.posts import PostRepository
from src.infrastructure.postgres.repositories.categories import CategoryRepository
from src.infrastructure.postgres.repositories.locations import LocationRepository
from src.schemas.posts import PostCreate, Post as PostSchema
from src.core.exceptions.domain_exceptions import DomainError, NotFoundError
from src.core.exceptions.infrastructure_exceptions import DatabaseError             
from src.infrastructure.postgres.models.users import User
from src.infrastructure.postgres.models.category import Category
from src.infrastructure.postgres.models.location import Location

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
                
                session.flush()
                session.refresh(post)
                
                post.author = session.get(User, author_id)
                post.category = session.get(Category, post_data.category_id)
                if post_data.location_id:
                    post.location = session.get(Location, post_data.location_id)
                
                return PostSchema.model_validate(post)
        
        except NotFoundError:
            raise
        except DatabaseError as e:
            raise DomainError(
                f"Ошибка базы данных при создании поста",
                details={"title": post_data.title, "error": str(e)}
            )
        except Exception as e:
            raise DomainError(
                f"Неизвестная ошибка при создании поста",
                details={"title": post_data.title, "error": str(e)}
            )