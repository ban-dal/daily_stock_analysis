# -*- coding: utf-8 -*-
"""Tests for the Naver Search news provider."""

import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock newspaper before search_service import (optional dependency)
if "newspaper" not in sys.modules:
    mock_np = MagicMock()
    mock_np.Article = MagicMock()
    mock_np.Config = MagicMock()
    sys.modules["newspaper"] = mock_np

from src.search_service import NaverSearchProvider


class TestNaverSearchProvider(unittest.TestCase):
    """Provider-specific request and response mapping behavior."""

    def _mock_response(self, payload, status_code: int = 200):
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = payload
        response.text = str(payload)
        return response

    def test_provider_maps_news_items_and_cleans_html(self) -> None:
        provider = NaverSearchProvider("client-id", "client-secret")

        with patch(
            "src.search_service._get_with_retry",
            return_value=self._mock_response(
                {
                    "items": [
                        {
                            "title": "<b>삼성전자</b> &amp; 반도체 실적",
                            "originallink": "https://news.example.com/samsung",
                            "link": "https://n.news.naver.com/article/001",
                            "description": "AI <b>수요</b> &quot;회복&quot;",
                            "pubDate": "Mon, 24 Jun 2026 09:30:00 +0900",
                        }
                    ]
                }
            ),
        ) as mock_get:
            resp = provider.search("삼성전자 005930.KS", max_results=5, days=3)

        self.assertTrue(resp.success)
        self.assertEqual(len(resp.results), 1)
        self.assertEqual(resp.results[0].title, "삼성전자 & 반도체 실적")
        self.assertEqual(resp.results[0].snippet, 'AI 수요 "회복"')
        self.assertEqual(resp.results[0].url, "https://news.example.com/samsung")
        self.assertEqual(resp.results[0].source, "news.example.com")
        self.assertEqual(resp.results[0].published_date, "Mon, 24 Jun 2026 09:30:00 +0900")
        params = mock_get.call_args.kwargs["params"]
        self.assertEqual(params["display"], 5)
        self.assertEqual(params["sort"], "date")
        headers = mock_get.call_args.kwargs["headers"]
        self.assertEqual(headers["X-Naver-Client-Id"], "client-id")
        self.assertEqual(headers["X-Naver-Client-Secret"], "client-secret")

    def test_provider_falls_back_to_naver_link_when_original_link_is_missing(self) -> None:
        provider = NaverSearchProvider("client-id", "client-secret")

        with patch(
            "src.search_service._get_with_retry",
            return_value=self._mock_response(
                {
                    "items": [
                        {
                            "title": "NAVER 실적 발표",
                            "link": "https://n.news.naver.com/article/002",
                            "description": "검색 광고 성장",
                            "pubDate": "Mon, 24 Jun 2026 10:00:00 +0900",
                        }
                    ]
                }
            ),
        ):
            resp = provider.search("NAVER 035420.KS", max_results=150, days=3)

        self.assertTrue(resp.success)
        self.assertEqual(resp.results[0].url, "https://n.news.naver.com/article/002")
        self.assertEqual(resp.results[0].source, "n.news.naver.com")

    def test_provider_requires_client_id_and_secret(self) -> None:
        self.assertFalse(NaverSearchProvider("client-id", "").is_available)
        self.assertFalse(NaverSearchProvider("", "client-secret").is_available)
        self.assertTrue(NaverSearchProvider("client-id", "client-secret").is_available)


if __name__ == "__main__":
    unittest.main()
