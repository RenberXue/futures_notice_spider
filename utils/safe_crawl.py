import time
from typing import Any, List, Dict

def safe_crawl(name: str, crawler: Any, retries: int = 1, delay: float = 3.0) -> List[Dict[str, str]]:
    for attempt in range(retries + 1):
        try:
            return crawler.crawl()
        except Exception as e:
            print(f"[{name}] 第 {attempt + 1} 次抓取失败: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print(f"[{name}] 最终抓取失败，返回空列表")
                return []