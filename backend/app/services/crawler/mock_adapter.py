from datetime import timedelta

from app.services.crawler.base import BaseCrawlerAdapter
from app.utils.time_utils import utc_now


LOCATIONS = [
    ("武汉市", "洪山区", "街道口", 30.526, 114.353, "地铁站太拥挤了，排队很久，真的有点烦。", "地铁"),
    ("武汉市", "江汉区", "协和医院", 30.584, 114.276, "医院排队等太久，信息提示不够清楚。", "医院"),
    ("武汉市", "武昌区", "楚河汉街", 30.555, 114.333, "商圈夜景很好看，逛街很开心。", "商圈"),
    ("武汉市", "东湖风景区", "东湖绿道", 30.557, 114.412, "绿道很清净，骑车特别放松。", "公园"),
    ("武汉市", "洪山区", "光谷广场", 30.505, 114.397, "晚高峰堵车严重，换乘也慢。", "交通"),
    ("武汉市", "硚口区", "同济医院", 30.579, 114.259, "导诊服务不错，候诊区更有序了。", "医院"),
    ("武汉市", "江岸区", "江汉路", 30.588, 114.299, "人流有点乱，餐饮排队太慢。", "商圈"),
    ("武汉市", "武昌区", "武汉大学", 30.539, 114.365, "校园很安静，樱花季体验不错。", "学校"),
]


class MockAdapter(BaseCrawlerAdapter):
    platform = "mock"

    async def search_posts(self, keyword: str, limit: int = 50) -> list[dict]:
        now = utc_now()
        posts = []
        platforms = ["weibo", "xhs", "douyin", "mock"]
        for index in range(limit):
            city, district, location, lat, lng, text, default_keyword = LOCATIONS[index % len(LOCATIONS)]
            platform = platforms[index % len(platforms)]
            posts.append(
                {
                    "platform": platform,
                    "keyword": keyword or default_keyword,
                    "raw_text": text,
                    "publish_time": (now - timedelta(hours=index % 48)).isoformat(),
                    "raw_location": f"{city}{district}{location}",
                    "city": city,
                    "district": district,
                    "location_name": location,
                    "lat": lat + (index % 5) * 0.001,
                    "lng": lng + (index % 4) * 0.001,
                    "like_count": 10 + index,
                    "comment_count": index % 12,
                    "share_count": index % 5,
                }
            )
        return posts
