import os
from playwright.sync_api import sync_playwright
from crawler.dce import DceCrawler
from crawler.czce import CzceCrawler
from crawler.shfe import ShfeCrawler
from crawler.cffex import CffexCrawler
from notifier.feishu import FeishuNotifier
from notifier.email import EmailNotifier
from utils.formatter import format_feishu_message, mark_sensitive, currenttime
from utils.filters import filter_today, filter_last_3_days, filter_latest_5
from utils.safe_crawl import safe_crawl

CRAWLERS = {
    "大商所": DceCrawler,
    "郑商所": CzceCrawler,
    "上期所": ShfeCrawler,
    "中金所": CffexCrawler
}

def run_crawlers():
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ))
        context.set_default_timeout(40000)

        for name, CrawlerClass in CRAWLERS.items():
            page = context.new_page()
            crawler = CrawlerClass(page)

            try:
                data = safe_crawl(name, crawler, retries=3, delay=5)
            except Exception as e:
                print(f"{name} 爬取失败: {e}")
                data = []
            marked_data = mark_sensitive(data)
            results[name] = marked_data
            page.close()
        browser.close()
    return results

def apply_filters(all_data):
    filtered = {}
    for ex, data in all_data.items():
        for item in data:
            if len(item["date"]) > 10:
                item["date"] = item["date"][:10].replace("-", "/").replace(".", "/")
            else:
                item["date"] = item["date"].replace("-", "/").replace(".", "/")
        filtered[ex] = data
    return filtered

def send_notifications(filtered_data, config):
    feishu_url = config.get("FEISHU_WEBHOOK")
    email_cfg = {
        "smtp_host": config.get("SMTP_HOST"),
        "smtp_port": int(config.get("SMTP_PORT", 25)),
        "username": config.get("SMTP_USER"),
        "password": config.get("SMTP_PASS"),
        "sender": config.get("EMAIL_SENDER"),
        "receivers": config.get("EMAIL_RECEIVERS", "").split(","),
    }

    feishu = FeishuNotifier(feishu_url)
    email = EmailNotifier(**email_cfg)

    # 发送三种筛选数据：
    # 1. 今日公告
    today_data = {ex: filter_today(data) for ex, data in filtered_data.items()}
    msg_today = format_feishu_message(today_data, "今日公告")
    feishu.send_message(msg_today)
    email.send_email(f"各期货交易所今日公告：[{currenttime()}]", msg_today)

    # 2. 近3天公告
    last3_data = {ex: filter_last_3_days(data) for ex, data in filtered_data.items()}
    msg_3d = format_feishu_message(last3_data, "近3天公告")
    feishu.send_message(msg_3d)
    email.send_email(f"各期货交易所近3天公告：[{currenttime()}]", msg_3d)

    # 3. 最新5条公告
    latest5_data = {ex: filter_latest_5(data) for ex, data in filtered_data.items()}
    msg_5 = format_feishu_message(latest5_data, "最新5条公告")
    feishu.send_message(msg_5)
    email.send_email(f"各期货交易所最新5条公告：[{currenttime()}]", msg_5)

def load_config():

    return {
        "FEISHU_WEBHOOK": os.getenv("FEISHU_WEBHOOK"),
        "SMTP_HOST": os.getenv("SMTP_HOST"),
        "SMTP_PORT": os.getenv("SMTP_PORT"),
        "SMTP_USER": os.getenv("SMTP_USER"),
        "SMTP_PASS": os.getenv("SMTP_PASS"),
        "EMAIL_SENDER": os.getenv("EMAIL_SENDER"),
        "EMAIL_RECEIVERS": os.getenv("EMAIL_RECEIVERS"),
    }

if __name__ == "__main__":
    config = load_config()
    all_data = run_crawlers()
    filtered = apply_filters(all_data)
    send_notifications(filtered, config)