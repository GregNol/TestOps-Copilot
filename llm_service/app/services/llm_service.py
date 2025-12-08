from openai import OpenAI
from app.config import settings


class LLMService:
    def __init__(self):
        if not settings.AI_MODEL_KEY:
            # Можно заменить на warning или оставить ошибку, если это критично
            print("⚠️ WARNING: AI_MODEL_KEY не задан")

        self.client = OpenAI(
            api_key=settings.AI_MODEL_KEY,
            base_url=settings.AI_MODEL_URL
        )
        self.model_name = settings.AI_MODEL_NAME

    def send_request(self, prompt: str) -> str:
        print(f"🧠 [LLMService] Запрос к {self.model_name}...")
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=8192,
                temperature=0.4,
                top_p=0.9
            )
            return response.choices[0].message.content or "Пустой ответ от модели"
        except Exception as e:
            print(f"❌ Ошибка LLM: {e}")
            raise e  # Пробрасываем ошибку выше, чтобы UseCase мог её обработать