from dependency_injector import containers, providers

from application.use_cases.yandex_auth import YandexAuthUseCase


class UseCasesContainer(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    repository = providers.DependenciesContainer()

    yandex_auth_use_case = providers.Factory(
        YandexAuthUseCase,
        yandex_auth_service=services.yandex_auth_service,
        user_repo=repository.user_repo
    )
