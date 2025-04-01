import os
import re
import uuid
from typing import Tuple
from pathlib import Path
from fastapi import UploadFile

from application.dto.files import FileCreateDTO
from domain.exceptions.file import UploadFileError


class UploadFileService:
    def __init__(self, upload_dir: str, extensions_file: str):
        self.base_dir = Path(upload_dir)
        self.extensions_file = tuple(extensions_file.split(','))

    def is_valid_extensions(self, filename: str) -> bool:
        return filename.lower().endswith(self.extensions_file)

    def _generate_unique_filename(self, original_filename: str, filename: str = None) -> Tuple[str, str]:
        """Генерирует уникальное имя файла, используя кастомное имя без расширения и оригинальное расширение."""
        extension = self._get_extension(original_filename)
        base_name = filename if filename else original_filename
        cleaned_base_name = self._sanitize_path(base_name)
        unique_name = f"{uuid.uuid4()}_{cleaned_base_name}{extension}"
        return unique_name, f"{cleaned_base_name}{extension}"

    @staticmethod
    def _sanitize_path(path_component: str) -> str:
        """Очищает компонент пути, убирая только пути и недопустимые символы, но сохраняет пробелы и кириллицу."""
        cleaned = os.path.basename(path_component)
        base_name, _ = os.path.splitext(cleaned)
        if not base_name or '..' in base_name or '/' in base_name or '\\' in base_name:
            raise ValueError(f"Invalid path component: {path_component}")
        return base_name.strip()

    async def _save_file(self, upload_dir: str, file_data: bytes, filename: str) -> str:
        """Сохраняет файл в указанной директории."""

        full_dir = self.base_dir / upload_dir
        full_dir.mkdir(parents=True, exist_ok=True)
        file_path = full_dir / filename
        if file_path.exists():
            raise UploadFileError(f"File already exists: {filename}")
        try:
            file_path.write_bytes(file_data)
            return str(file_path)
        except Exception as e:
            raise UploadFileError(f"Failed to save file: {str(e)}")

    @staticmethod
    def _get_extension(filename: str) -> str:
        """Извлекает расширение из оригинального имени файла."""
        _, extension = os.path.splitext(filename)
        return extension

    @staticmethod
    def _extract_filename(full_path: str) -> str:
        """Извлекает имя файла из полного пути."""
        path = Path(full_path)
        return path.name

    async def upload(self, upload_dir: str, file: UploadFile, filename: str = None) -> FileCreateDTO:
        """Основной метод для загрузки аудио-файла."""
        if not self.is_valid_extensions(file.filename):
            raise UploadFileError(f"Only files are allowed {','.join(self.extensions_file)}")

        file_data = await file.read()
        unique_name, original_name = self._generate_unique_filename(file.filename, filename)
        file_path = await self._save_file(upload_dir, file_data, unique_name)

        return FileCreateDTO(
            filename=unique_name,
            path=file_path,
            original_name=original_name
        )

    async def delete_file(self, upload_dir: str, full_path: str) -> dict:
        """Удаляет конкретный файл пользователя."""

        filename = self._extract_filename(full_path)
        file_path = self.base_dir / upload_dir / filename
        if not file_path.exists():
            raise UploadFileError(f"File not found: {filename}")
        try:
            file_path.unlink()
            return {"message": f"File {filename} deleted successfully"}
        except Exception as e:
            raise UploadFileError(f"Failed to delete file: {str(e)}")
