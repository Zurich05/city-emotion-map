from app.services.crawler.douyin_adapter import DouyinAdapter
from app.services.crawler.mock_adapter import MockAdapter
from app.services.crawler.weibo_adapter import WeiboAdapter
from app.services.crawler.xhs_adapter import XhsAdapter


ADAPTERS = {
    "mock": MockAdapter,
    "weibo": WeiboAdapter,
    "xhs": XhsAdapter,
    "douyin": DouyinAdapter,
}


def get_adapter(platform: str):
    return ADAPTERS.get(platform, MockAdapter)()
