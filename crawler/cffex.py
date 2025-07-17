from crawler.base import BaseCrawler

class CffexCrawler(BaseCrawler):
    def crawl(self):
        self.page.goto("http://www.cffex.com.cn/jystz/")
        self.page.wait_for_selector("ul.clearFloat")

        items = self.page.query_selector_all("ul.clearFloat li")
        data = []
        for item in items:
            a = item.query_selector("a.list_a_text")
            date_node = item.query_selector("a.time.comparetime")
            if not a or not date_node:
                continue
            title = a.inner_text().strip()
            href = a.get_attribute("href")
            date = date_node.inner_text().strip()
            if href and not href.startswith("http"):
                href = "http://www.cffex.com.cn" + href
            data.append({"title": title, "link": href, "date": date})
        return data