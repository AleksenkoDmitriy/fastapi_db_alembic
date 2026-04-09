from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.posts import PostCreate, Post as PostSchema
from src.core.exceptions import DomainError, NotFoundError, DatabaseError


class CreatePost:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()
        self._category_repo = CategoryRepository()
        self._user_repo = UserRepository()

    async def execute(self, post_data: PostCreate) -> PostSchema:
        try:
            with self._database.session() as session:
                category = self._category_repo.get_by_id(session, post_data.category_id)
                if not category:
                    raise NotFoundError(
                        entity_name="Категория",
                        field="id",
                        value=str(post_data.category_id)
                    )
                
                author = self._user_repo.get_by_id(session, post_data.author_id)
                if not author:
                    raise NotFoundError(
                        entity_name="Автор",
                        field="id",
                        value=str(post_data.author_id)
                    )
                
                post = self._repo.create(session, **post_data.model_dump())
                
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