from crawler.base import BaseCrawler

class CzceCrawler(BaseCrawler):
    def crawl(self):
        self.page.goto("http://app.czce.com.cn/cms/pub/search/searchdtnew.jsp?channelcode=H770103")
        self.page.wait_for_selector("td.xxgktit")

        rows = self.page.query_selector_all("tr")
        data = []
        for row in rows:
            title_cell = row.query_selector("td.xxgktit")
            date_cell = row.query_selector("td.xxgktd1")
            if title_cell and date_cell:
                link = title_cell.query_selector("a")
                title = link.inner_text()
                href = link.get_attribute("href")
                date = date_cell.inner_text()
                data.append({"title": title, "link": href, "date": date})
        return data