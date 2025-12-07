import aiohttp
import yaml
import json
import logging

logger = logging.getLogger(__name__)


class OpenAPIService:
    async def fetch_spec(self, url: str) -> str:
        """Загрузка по URL (оставляем для обратной совместимости, если нужно)"""
        # ... (код из предыдущего шага) ...
        pass

    def validate_and_parse_file(self, file_content: bytes, filename: str) -> str:
        """
        Парсит байтовый контент файла (JSON/YAML) в строку.
        """
        try:
            # 1. Декодируем байты в строку
            text_content = file_content.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: File encoding is not UTF-8."

        # 2. Пытаемся определить формат по расширению или контенту
        is_yaml = filename.endswith(
            ('.yaml', '.yml')) or not text_content.strip().startswith('{')

        try:
            if is_yaml:
                # Парсим YAML -> Python Dict -> JSON String
                data = yaml.safe_load(text_content)
            else:
                # Парсим JSON -> Python Dict
                data = json.loads(text_content)

            # Проверка, что это похожу на Swagger/OpenAPI
            if not isinstance(data, dict) or not any(k in data for k in ['openapi', 'swagger', 'paths']):
                return "Error: The file does not look like a valid OpenAPI/Swagger specification."

            # Конвертируем обратно в JSON-строку (минифицированную) для LLM
            return json.dumps(data, ensure_ascii=False)

        except (json.JSONDecodeError, yaml.YAMLError) as e:
            return f"Error parsing file: {str(e)}"
