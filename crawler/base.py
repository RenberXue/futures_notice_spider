from playwright.sync_api import Page
from typing import List, Dict

class BaseCrawler:
    def __init__(self, page: Page):
        self.page = page

    def crawl(self) -> List[Dict[str, str]]:
        raise NotImplementedError("Each crawler must implement the crawl method")