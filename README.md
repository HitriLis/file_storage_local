# File Storage Local

**File Storage Local** — это приложение на Python для локального хранения файлов, предоставляющее API для загрузки, скачивания и управления файлами на вашем сервере.

## Возможности

- **Загрузка файлов**: Позволяет загружать файлы на сервер через API.
- **Скачивание файлов**: Предоставляет возможность скачивать файлы с сервера.
- **Удаление файлов**: Поддерживает удаление файлов с сервера.
- **Список файлов**: Позволяет получать список всех сохраненных файлов.

## Установка
1. **Клонируйте репозиторий**:

    ```bash
    git clone https://github.com/HitriLis/file_storage_local.git
    ```

2. **Перейдите в директорию проекта**:

    ```bash
    cd file_storage_local
    ```
3. **Настройте переменные окружения**:

    - В корневой директории проекта уже есть файл `.env.example`.  
      Скопируйте его в `.env` и заполните своими данными:

      ```bash
      cp .env.example .env
      ```

    - Откройте `.env` и укажите нужные параметры:

      ```ini
      # Конфигурация базы данных
      DB_USER=your_db_user
      DB_PASSWORD=your_db_password
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=your_db_name

      # JWT-токены
      SECRET_KEY=your_secret_key
      ALGORITHM=HS256
      ACCESS_TOKEN_EXPIRE_MINUTES=30
      REFRESH_TOKEN_EXPIRE_DAYS=7

      # Yandex OAuth
      YANDEX_CLIENT_ID=your_yandex_client_id
      YANDEX_CLIENT_SECRET=your_yandex_client_secret
      YANDEX_REDIRECT_URI=http://localhost:8000/auth/yandex/callback

      # Настройки файлов
      UPLOAD_DIR=./storage
      EXTENSIONS_FILE=.jpg,.png,.pdf,.docx
      ```

    ⚠️ **Важно!** Не загружайте `.env` в репозиторий — он уже добавлен в `.gitignore`.

## Docker

1. **Запустите приложение**:
    ```bash
    docker-compose up -d
    ```

## Настройки

- **Переменные окружения**  
  Все настройки хранятся в файле `.env`, который можно создать из `.env.example`.

- **Директория хранения файлов**  
  По умолчанию файлы сохраняются в директории `storage`. Вы можете изменить путь в `.env`:

    ```ini
    UPLOAD_DIR=/path/to/storage
    ```

- **Допустимые расширения файлов**  
  Можно ограничить загрузку файлов по их расширению:

    ```ini
    EXTENSIONS_FILE=.jpg,.png,.pdf,.docx
    ```

- **Изменение порта**  
  Приложение по умолчанию запускается на порту `8000`, но если вы используете `docker-compose`, измените порт в `docker-compose.yml`:

    ```yaml
    services:
      app:
        ports:
          - "8080:8000"  # Измените 8080 на нужный порт
    ```

  После изменения перезапустите контейнер:

    ```bash
    docker-compose up -d --build
    ```
