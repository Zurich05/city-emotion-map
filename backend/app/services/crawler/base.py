from abc import ABC, abstractmethod


class BaseCrawlerAdapter(ABC):
    platform: str

    @abstractmethod
    async def search_posts(self, keyword: str, limit: int = 50) -> list[dict]:
        raise NotImplementedError
