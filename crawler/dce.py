from crawler.base import BaseCrawler

class DceCrawler(BaseCrawler):
    def crawl(self):
        self.page.goto("http://www.dce.com.cn/dalianshangpin/ywfw/jystz/ywtz/index.html")
        self.page.wait_for_selector("ul.list_tpye06")

        items = self.page.query_selector_all("ul.list_tpye06 li")
        data = []
        for li in items:
            date = li.query_selector("span").inner_text().strip()
            a = li.query_selector("a")
            title = a.inner_text().strip()
            href = a.get_attribute("href")
            if href and not href.startswith("http"):
                href = "http://www.dce.com.cn" + href
            data.append({"title": title, "link": href, "date": date})
        return data