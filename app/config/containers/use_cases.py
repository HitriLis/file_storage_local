from dependency_injector import containers, providers

from application.use_cases.upload_file import UploadFileUseCase, DeleteFileUseCase
from application.use_cases.yandex_auth import YandexAuthUseCase


class UseCasesContainer(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    repository = providers.DependenciesContainer()

    yandex_auth_use_case = providers.Factory(
        YandexAuthUseCase,
        yandex_auth_service=services.yandex_auth_service,
        user_repo=repository.user_repo
    )

    upload_file = providers.Factory(
        UploadFileUseCase,
        upload_service=services.upload_service,
        file_repo=repository.file_repo
    )

    delete_file = providers.Factory(
        DeleteFileUseCase,
        upload_service=services.upload_service,
        file_repo=repository.file_repo
    )
