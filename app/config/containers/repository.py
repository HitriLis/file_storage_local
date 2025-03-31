from dependency_injector import containers, providers
from infrastructure.database.repositories.user import SQLAlchemyUserRepository


class RepositoryContainer(containers.DeclarativeContainer):
    database = providers.DependenciesContainer()

    user_repo = providers.Factory(
        SQLAlchemyUserRepository,
        session=database.session
    )

