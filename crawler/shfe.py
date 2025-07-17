from crawler.base import BaseCrawler

class ShfeCrawler(BaseCrawler):
    def crawl(self):
        self.page.goto("https://www.shfe.com.cn/publicnotice/notice/")
        self.page.wait_for_selector("div.table_item_info")

        items = self.page.query_selector_all("div.table_item_info")
        data = []
        for item in items:
            a = item.query_selector(".info_item_title a")
            date_node = item.query_selector(".info_item_date")
            if not a or not date_node:
                continue
            title = a.inner_text().strip()
            href = a.get_attribute("href")
            date = date_node.inner_text().strip()
            if href and not href.startswith("http"):
                href = "https://www.shfe.com.cn/publicnotice/notice" + href.lstrip(".")
            data.append({"title": title, "link": href, "date": date})
        return data