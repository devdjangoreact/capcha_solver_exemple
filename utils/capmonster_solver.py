from typing import Any, Dict, Optional

from base_solver import BaseCaptchaSolver


class CapMonsterSolver(BaseCaptchaSolver):
    """CapMonster captcha solving service implementation"""

    API_URL = "https://api.capmonster.cloud"

    def solve_hcaptcha(self, site_url: str, site_key: str) -> Optional[str]:
        """Solve hCaptcha using CapMonster service"""
        self.logger.info("Solving hCaptcha with CapMonster")

        # Create task
        task_data = {
            "clientKey": self.api_key,
            "task": {
                "type": "RecaptchaV2Task",
                "websiteURL": site_url,
                "websiteKey": site_key,
            },
        }

        if self.proxy:
            task_data["task"]["proxyType"] = "http"
            task_data["task"]["proxyAddress"] = self.proxy.split("://")[1].split(":")[0]
            task_data["task"]["proxyPort"] = int(self.proxy.split(":")[2].split("@")[0])
            if "@" in self.proxy and ":" in self.proxy:
                auth_parts = self.proxy.split("://")[1].split("@")[0].split(":")
                if len(auth_parts) == 2:
                    task_data["task"]["proxyLogin"] = auth_parts[0]
                    task_data["task"]["proxyPassword"] = auth_parts[1]

        create_response = self._make_request(f"{self.API_URL}/createTask", task_data)
        if not create_response or "taskId" not in create_response:
            self.logger.error("Failed to create CapMonster task")
            return None

        task_id = create_response["taskId"]
        self.logger.info(f"Task created with ID: {task_id}")

        # Wait for solution
        return self._wait_for_solution(
            task_id, f"{self.API_URL}/getTaskResult", max_attempts=120, interval=5
        )
