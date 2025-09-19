from typing import Any, Dict, Optional

from base_solver import BaseCaptchaSolver


class CapsolverSolver(BaseCaptchaSolver):
    """Capsolver service implementation"""

    API_URL = "https://api.capsolver.com"

    def solve_hcaptcha(self, site_url: str, site_key: str) -> Optional[str]:
        """Solve hCaptcha using Capsolver service"""
        self.logger.info("Solving hCaptcha with Capsolver")

        task_data = {
            "clientKey": self.api_key,
            "task": {
                "type": "HCaptchaTask",
                "websiteURL": site_url,
                "websiteKey": site_key,
            },
        }

        if self.proxy:
            task_data["task"]["proxy"] = self.proxy

        create_response = self._make_request(f"{self.API_URL}/createTask", task_data)
        if not create_response or "taskId" not in create_response:
            self.logger.error("Failed to create Capsolver task")
            return None

        task_id = create_response["taskId"]
        self.logger.info(f"Task created with ID: {task_id}")

        # Wait for solution
        return self._wait_for_solution(
            task_id, f"{self.API_URL}/getTaskResult", max_attempts=120, interval=5
        )
