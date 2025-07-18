from typing import List, Dict
from datetime import datetime, timedelta

def filter_today(data: List[Dict]) -> List[Dict]:
    today = datetime.now().date()
    return [item for item in data if datetime.strptime(item["date"], "%Y/%m/%d").date() == today]

def filter_last_3_days(data: List[Dict]) -> List[Dict]:
    today = datetime.now().date()
    three_days_ago = today - timedelta(days=3)
    return [item for item in data if three_days_ago <= datetime.strptime(item["date"], "%Y/%m/%d").date() <= today]

def filter_latest_5(data: List[Dict]) -> List[Dict]:
    # 先按日期降序，再取前5
    sorted_list = sorted(data, key=lambda x: x["date"], reverse=True)
    return sorted_list[:5]