import aiohttp
import asyncio
from bs4 import BeautifulSoup


class HTMLService:
    @staticmethod
    def _clean_structure(html_content: str) -> str:
        """Синхронная очистка DOM (CPU-bound операция)."""
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, 'html.parser')

        # Удаление мусора
        for tag in soup(['script', 'style', 'noscript', 'iframe', 'meta', 'link']):
            tag.decompose()

        # Упрощение медиа-контента
        for img in soup.find_all('img'):
            alt = img.get('alt', 'No Alt')
            img.replace_with(f'[IMG: {alt}]')

        for a in soup.find_all('a'):
            text = a.get_text(strip=True)
            a.replace_with(f'[LINK: {text}]')  # Ссылки можно даже не оставлять url, если они не важны

        # Получаем текст, но сохраняем структуру блоков
        return soup.get_text(separator='\n', strip=True)

    async def fetch_page(self, url: str) -> str:
        """Асинхронная загрузка и очистка страницы."""
        headers = {'User-Agent': 'QA-Bot/1.0'}
        print(f"🌐 [HTMLService] Загрузка: {url}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=20) as response:
                    if response.status != 200:
                        print(f"❌ Ошибка статуса: {response.status}")
                        return ""
                    html_text = await response.text()

                    # Запускаем очистку в отдельном потоке, чтобы не блочить Event Loop
                    clean_text = await asyncio.to_thread(self._clean_structure, html_text)
                    return clean_text
        except Exception as e:
            print(f"❌ Ошибка сети: {e}")
            return ""