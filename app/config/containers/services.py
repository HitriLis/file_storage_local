from dependency_injector import containers, providers

from application.services.auth_service import AuthTokenService
from application.services.files import FileService
from application.services.upload_file import UploadFileService
from application.services.user_service import UserService
from infrastructure.services.yandex_auth_service import YandexAuthService


class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repository = providers.DependenciesContainer()

    yandex_auth_service = providers.Singleton(
        YandexAuthService,
        client_id=config.YANDEX_CLIENT_ID,
        client_secret=config.YANDEX_CLIENT_SECRET,
        redirect_uri=config.YANDEX_REDIRECT_URI,
    )
    auth_service = providers.Singleton(
        AuthTokenService,
        secret_key=config.SECRET_KEY,
        algorithm=config.ALGORITHM,
        access_token_expire_minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=config.REFRESH_TOKEN_EXPIRE_DAYS
    )

    user_service = providers.Singleton(
        UserService,
        user_repo=repository.user_repo
    )

    file_service = providers.Singleton(
        FileService,
        file_repo=repository.file_repo
    )

    upload_service = providers.Singleton(
        UploadFileService,
        upload_dir=config.UPLOAD_DIR,
        extensions_file=config.EXTENSIONS_FILE
    )
