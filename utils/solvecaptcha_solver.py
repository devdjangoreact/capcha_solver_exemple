import time
from typing import Any, Dict, Optional

from base_solver import BaseCaptchaSolver


class SolveCaptchaSolver(BaseCaptchaSolver):
    """SolveCaptcha service implementation"""

    API_URL = "https://api.solvecaptcha.com"

    def solve_hcaptcha(self, site_url: str, site_key: str) -> Optional[str]:
        """Solve hCaptcha using SolveCaptcha service"""
        self.logger.info("Solving hCaptcha with SolveCaptcha")

        task_data = {
            "key": self.api_key,
            "method": "hcaptcha",
            "pageurl": site_url,
            "sitekey": site_key,
            "json": 1,
        }

        if self.proxy:
            task_data["proxy"] = self.proxy

        create_response = self._make_request(f"{self.API_URL}/in.php", task_data)
        if not create_response or create_response.get("status") != 1:
            self.logger.error("Failed to create SolveCaptcha task")
            return None

        task_id = create_response["request"]
        self.logger.info(f"Task created with ID: {task_id}")

        # Wait for solution
        return self._wait_for_solution(
            task_id, f"{self.API_URL}/res.php", max_attempts=120, interval=5
        )

    def _wait_for_solution(
        self, task_id: str, check_url: str, max_attempts: int = 60, interval: int = 3
    ) -> Optional[str]:
        """Custom wait implementation for SolveCaptcha"""
        for attempt in range(max_attempts):
            try:
                data = {"key": self.api_key, "action": "get", "id": task_id, "json": 1}

                result = self._make_request(check_url, data)
                if not result:
                    continue

                if result.get("status") == 1:
                    return result.get("request")

                time.sleep(interval)

            except Exception as e:
                self.logger.error(f"Error checking solution: {e}")
                time.sleep(interval)

        self.logger.error("Captcha solution timeout")
        return None
