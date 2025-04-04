from dependency_injector import containers, providers

from .containers.database import DatabaseContainer
from .containers.repository import RepositoryContainer
from .containers.services import ServicesContainer
from .containers.use_cases import UseCasesContainer
from .settings import settings
from .database import db_settings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(default={
        "YANDEX_CLIENT_ID": settings.YANDEX_CLIENT_ID,
        "YANDEX_CLIENT_SECRET": settings.YANDEX_CLIENT_SECRET,
        "YANDEX_REDIRECT_URI": settings.YANDEX_REDIRECT_URI,
        "SECRET_KEY": settings.SECRET_KEY,
        "ALGORITHM": settings.ALGORITHM,
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "REFRESH_TOKEN_EXPIRE_DAYS": int(settings.REFRESH_TOKEN_EXPIRE_DAYS),
        "UPLOAD_DIR": settings.UPLOAD_DIR,
        "EXTENSIONS_FILE": settings.EXTENSIONS_FILE
    })

    config_db = providers.Configuration(default={
        "POOL_SIZE": db_settings.POOL_SIZE,
        "ECHO_SQL": db_settings.ECHO_SQL,
        "DB_URL": db_settings.db_url,
    })

    database = providers.Container(
        DatabaseContainer,
        config=config_db
    )
    repository = providers.Container(
        RepositoryContainer,
        database=database
    )

    services = providers.Container(
        ServicesContainer,
        config=config,
        repository=repository
    )
    use_cases = providers.Container(
        UseCasesContainer,
        services=services,
        repository=repository
    )
