import json
import logging
import random
from typing import Any, Dict, List, Optional

from camoufox.sync_api import Camoufox
from playwright.sync_api import Browser, BrowserContext, Page


class BrowserManager:
    """Browser manager with anti-detection features and proxy support"""

    def __init__(self, headless: bool = True, proxy: Optional[str] = None):
        self.headless = headless
        self.proxy = proxy
        self.playwright = None
        self.browser = None
        self.context = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()

    def start(self):
        """Start browser with anti-detection settings"""
        user_data_dir = "brouser_dir"
        self.playwright = Camoufox(
            window=(1282, 955),
            persistent_context=True,
            user_data_dir=user_data_dir,
            i_know_what_im_doing=True,
            geoip=True,
            # humanize=3.0,
            enable_cache=True,
        ).start()

        self.context = self.playwright

        self.logger.info("Browser started with anti-detection features")

    def stop(self):
        """Stop browser and cleanup"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.logger.info("Browser stopped")

    def new_page(self) -> Page:
        """Create new page with anti-detection features"""
        if not self.context:
            raise RuntimeError("Browser context not initialized")

        page = self.context.new_page()

        # Override webdriver property
        page.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """
        )

        # Override plugins
        page.add_init_script(
            """
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """
        )

        return page

    def _get_random_user_agent(self) -> str:
        """Get random user agent for better anonymity"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
        ]
        return random.choice(user_agents)
