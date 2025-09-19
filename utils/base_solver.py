import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import requests


class BaseCaptchaSolver(ABC):
    """Abstract base class for all captcha solving services"""

    def __init__(self, api_key: str, proxy: Optional[str] = None):
        self.api_key = api_key
        self.proxy = proxy
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def solve_hcaptcha(self, site_url: str, site_key: str) -> Optional[str]:
        """Solve hCaptcha and return the solution token"""
        pass

    def _make_request(self, url: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make HTTP request to captcha service API"""
        try:
            proxies = None
            if self.proxy:
                proxies = {"http": self.proxy, "https": self.proxy}

            response = requests.post(url, json=data, proxies=proxies, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            return None

    def _wait_for_solution(
        self, task_id: str, check_url: str, max_attempts: int = 60, interval: int = 3
    ) -> Optional[str]:
        """Wait for captcha solution to be ready"""
        for attempt in range(max_attempts):
            try:
                data = {"clientKey": self.api_key, "taskId": task_id}

                result = self._make_request(check_url, data)
                if not result:
                    continue

                if result.get("status") == "ready":
                    return result.get("solution", {}).get(
                        "gRecaptchaResponse"
                    ) or result.get("solution", {}).get("token")

                time.sleep(interval)

            except Exception as e:
                self.logger.error(f"Error checking solution: {e}")
                time.sleep(interval)

        self.logger.error("Captcha solution timeout")
        return None
