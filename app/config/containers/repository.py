from dependency_injector import containers, providers
from infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository


# class RepositoryContainer(containers.DeclarativeContainer):
#     user_repository = providers.Factory(
#         SQLAlchemyUserRepository
#     )

