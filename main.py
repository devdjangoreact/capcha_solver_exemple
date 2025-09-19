import logging
import os
import time
from typing import Any, Callable, Dict, Optional

from dotenv import load_dotenv
from playwright.sync_api import Page

from utils.browser_manager import BrowserManager
from utils.capmonster_solver import CapMonsterSolver
from utils.capsolver_solver import CapsolverSolver
from utils.solvecaptcha_solver import SolveCaptchaSolver

# Load environment variables
load_dotenv()


class CaptchaAutomation:
    """Main automation class for handling Incapsula/hCaptcha with various solving services"""

    def __init__(
        self,
        solver_type: str = None,
        api_key: str = None,
        proxy: str = None,
        headless: bool = True,
    ):

        # Get values from environment variables or use defaults
        self.solver_type = solver_type or os.getenv("SOLVER_TYPE", "capmonster").lower()
        self.api_key = api_key or os.getenv("API_KEY")
        self.proxy = proxy or os.getenv("PROXY")
        self.headless = os.getenv("HEADLESS", "True").lower() == "true"
        self.target_url = os.getenv("TARGET_URL", "https://example.com")

        self.browser_manager = None
        self.captcha_solver = None

        # Setup logging
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(self.__class__.__name__)

        # Validate required parameters
        if not self.api_key:
            raise ValueError("API_KEY is required in .env file or constructor")

        if not self.target_url or self.target_url == "https://example.com":
            raise ValueError("TARGET_URL is required in .env file")

        # Initialize captcha solver
        self._init_captcha_solver()

    def _init_captcha_solver(self):
        """Initialize the appropriate captcha solver"""
        if self.solver_type == "capmonster":
            self.captcha_solver = CapMonsterSolver(self.api_key, self.proxy)
        elif self.solver_type == "solvecaptcha":
            self.captcha_solver = SolveCaptchaSolver(self.api_key, self.proxy)
        elif self.solver_type == "capsolver":
            self.captcha_solver = CapsolverSolver(self.api_key, self.proxy)
        else:
            raise ValueError(f"Unknown solver type: {self.solver_type}")

        self.logger.info(f"Initialized {self.solver_type} solver")

    def solve_incapsula_captcha(self, url: str = None, max_attempts: int = 3) -> bool:
        """Main method to solve Incapsula captcha on a given URL"""
        target_url = url or self.target_url

        for attempt in range(max_attempts):
            try:
                self.logger.info(
                    f"Attempt {attempt + 1}/{max_attempts} for {target_url}"
                )

                with BrowserManager(
                    headless=self.headless, proxy=self.proxy
                ) as browser_manager:
                    pages = browser_manager.playwright.pages
                    if pages:
                        page = pages[0]
                    else:
                        page = browser_manager.new_page()

                    # Navigate to target URL
                    page.goto(target_url, wait_until="networkidle")
                    self.logger.info(f"Navigated to {target_url}")

                    # Check if captcha is present
                    if self._is_captcha_present(page):
                        self.logger.info("Captcha detected, attempting to solve...")

                        # Extract captcha information
                        site_key = self._extract_site_key(page)
                        if not site_key:
                            self.logger.error("Failed to extract site key")
                            continue

                        self.logger.info(f"Extracted site key: {site_key}")

                        # Solve captcha
                        solution = self.captcha_solver.solve_hcaptcha(
                            target_url, site_key
                        )
                        if not solution:
                            self.logger.error("Failed to solve captcha")
                            continue

                        self.logger.info("Captcha solution received")

                        # Submit solution
                        if self._submit_solution(page, solution):
                            self.logger.info("Captcha solved successfully!")
                            return True
                        else:
                            self.logger.warning("Solution submission failed")

                    else:
                        self.logger.info("No captcha detected, proceeding...")
                        return True

            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(5)

        self.logger.error("All attempts failed")
        return False

    def _is_captcha_present(self, page: Page) -> bool:
        """Check if hCaptcha is present on the page"""
        try:
            # Check for various captcha indicators
            selectors = [
                'iframe[src*="incapsula"]',
                'iframe[src*="hcaptcha"]',
                "[data-sitekey]",
                ".h-captcha",
                ".g-recaptcha",
                "#captcha",
                ".captcha-container",
            ]

            for selector in selectors:
                if page.query_selector(selector):
                    return True

            # Check page content
            content = page.content()
            captcha_indicators = ["hcaptcha", "incapsula", "captcha", "challenge"]
            for indicator in captcha_indicators:
                if indicator in content.lower():
                    return True

            return False

        except Exception as e:
            self.logger.error(f"Error checking captcha presence: {e}")
            return False

    def _extract_site_key(self, page: Page) -> Optional[str]:
        """Extract hCaptcha site key from the page"""
        try:
            # Try to find site key in iframe
            iframe = page.query_selector('iframe[src*="hcaptcha"]')
            if iframe:
                src = iframe.get_attribute("src")
                if src and "sitekey=" in src:
                    return src.split("sitekey=")[1].split("&")[0]

            # Try to find site key in data attributes
            captcha_div = page.query_selector("[data-sitekey]")
            if captcha_div:
                return captcha_div.get_attribute("data-sitekey")

            # Try to find in script tags
            script_content = page.content()
            if "sitekey" in script_content:
                import re

                matches = re.findall(
                    r'sitekey["\']?:\s*["\']([^"\']+)["\']', script_content
                )
                if matches:
                    return matches[0]

            # Check for hidden inputs
            hidden_inputs = page.query_selector_all('input[type="hidden"]')
            for input in hidden_inputs:
                name = input.get_attribute("name")
                value = input.get_attribute("value")
                if name and "sitekey" in name.lower() and value:
                    return value

            return None

        except Exception as e:
            self.logger.error(f"Error extracting site key: {e}")
            return None

    def _submit_solution(self, page: Page, solution: str) -> bool:
        """Submit captcha solution to the page"""
        try:
            # Execute solution in browser context
            result = page.evaluate(
                f"""
                (function(solution) {{
                    try {{
                        // Try to find h-captcha response textarea
                        const textareas = document.querySelectorAll('textarea[name="h-captcha-response"]');
                        if (textareas.length > 0) {{
                            textareas[0].value = solution;
                            textareas[0].style.display = 'block';
                            console.log('Found h-captcha-response textarea');
                        }}
                        
                        // Try to find g-recaptcha-response
                        const gTextareas = document.querySelectorAll('textarea[name="g-recaptcha-response"]');
                        if (gTextareas.length > 0) {{
                            gTextareas[0].value = solution;
                            gTextareas[0].style.display = 'block';
                            console.log('Found g-recaptcha-response textarea');
                        }}
                        
                        // Dispatch change events
                        const event = new Event('change', {{ bubbles: true }});
                        if (textareas[0]) textareas[0].dispatchEvent(event);
                        if (gTextareas[0]) gTextareas[0].dispatchEvent(event);
                        
                        // Try to find and click submit button
                        const submitButtons = document.querySelectorAll('button[type="submit"], input[type="submit"]');
                        if (submitButtons.length > 0) {{
                            submitButtons[0].click();
                            console.log('Clicked submit button');
                            return true;
                        }}
                        
                        // Try to submit form
                        const forms = document.querySelectorAll('form');
                        if (forms.length > 0) {{
                            forms[0].submit();
                            console.log('Submitted form');
                            return true;
                        }}
                        
                        return false;
                    }} catch (error) {{
                        console.error('Error submitting solution:', error);
                        return false;
                    }}
                }})('{solution}');
            """
            )

            # Wait for navigation or changes
            page.wait_for_timeout(3000)

            # Check if we're still on captcha page
            if not self._is_captcha_present(page):
                return True

            return result or False

        except Exception as e:
            self.logger.error(f"Error submitting solution: {e}")
            return False


# Example usage
if __name__ == "__main__":
    try:
        # Create automation instance with settings from .env
        automation = CaptchaAutomation()

        # Run captcha solving
        success = automation.solve_incapsula_captcha()

        if success:
            print("✅ Automation completed successfully!")
        else:
            print("❌ Automation failed")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your .env configuration")
