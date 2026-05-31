from app.services.crawler.mock_adapter import MockAdapter


class DouyinAdapter(MockAdapter):
    platform = "douyin"

    async def search_posts(self, keyword: str, limit: int = 50) -> list[dict]:
        posts = await super().search_posts(keyword, limit)
        for post in posts:
            post["platform"] = self.platform
        return posts
