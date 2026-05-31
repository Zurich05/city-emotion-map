import unittest

from app.services.sentiment_service import SentimentService
from app.services.statistics_service import calculate_risk_level
from app.utils.hash import text_hash
from app.utils.privacy import mask_coordinate
from app.utils.text_cleaner import clean_text


class CoreServiceTests(unittest.TestCase):
    def test_clean_text_removes_noise_and_sensitive_data(self):
        text = "<p>今天地铁站太挤了 https://example.com 手机13812345678 地址武汉市洪山区珞喻路123号</p>"

        result = clean_text(text)

        self.assertNotIn("https://", result)
        self.assertNotIn("13812345678", result)
        self.assertNotIn("123号", result)
        self.assertIn("地铁站太挤了", result)

    def test_mask_coordinate_keeps_four_decimal_places_by_default(self):
        self.assertEqual(mask_coordinate(114.3536789), 114.3537)

    def test_text_hash_is_stable_and_normalizes_spaces(self):
        self.assertEqual(text_hash(" 地铁  太挤 "), text_hash("地铁 太挤"))

    def test_local_sentiment_detects_negative_stress(self):
        service = SentimentService()

        result = service.analyze_text_sync("今天地铁站太拥挤了，排队很久，真的有点烦。")

        self.assertEqual(result["sentiment_label"], "negative")
        self.assertLess(result["sentiment_score"], 0)
        self.assertGreater(result["stress_score"], 0)
        self.assertGreater(result["anger_score"], 0)

    def test_risk_level_rules(self):
        self.assertEqual(calculate_risk_level(20, 0.71, 10, 20), "high")
        self.assertEqual(calculate_risk_level(10, 0.5, 3, 10), "medium")
        self.assertEqual(calculate_risk_level(3, 0.8, 1, 3), "low")


if __name__ == "__main__":
    unittest.main()
