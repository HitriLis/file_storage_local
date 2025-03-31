from dependency_injector import containers, providers
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
        "REFRESH_TOKEN_EXPIRE_DAYS": int(settings.REFRESH_TOKEN_EXPIRE_DAYS)
    })
    config_db = providers.Object(db_settings)
    services = providers.Container(
        ServicesContainer,
        config=config
    )
    use_cases = providers.Container(
        UseCasesContainer,
        services=services,
    )
