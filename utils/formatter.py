from typing import Dict, List
from datetime import datetime

def format_date(date_str: str) -> str:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y/%m/%d")
        except Exception:
            continue
    return date_str

def format_feishu_message(data: Dict[str, List[Dict]], filter_name: str) -> str:

    has_ann = [k for k,v in data.items() if len(v) > 0]
    no_ann = [k for k,v in data.items() if len(v) == 0]

    msg = f"{filter_name}：\n\n"

    if has_ann:
        msg += "以下交易所有公告：\n"
        for ex in has_ann:
            msg += f"- {ex}\n"
    if no_ann:
        msg += "\n以下交易所无公告：\n"
        for ex in no_ann:
            msg += f"- {ex}\n"

    for ex in has_ann:
        ann_list = data[ex]

        ann_list = sorted(ann_list, key=lambda x: x["date"], reverse=True)
        msg += f"\n以下是{ex} {format_date(ann_list[0]['date'])}号的公告：\n"
        for i, ann in enumerate(ann_list, 1):
            title = ann["title"]
            link = ann["link"]
            date = format_date(ann["date"])
            msg += f"{i}. [{title}]({link}) 时间：{date}\n"

    return msg