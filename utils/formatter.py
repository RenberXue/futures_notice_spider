from typing import Dict, List
from datetime import datetime
import pytz

SENSITIVE_KEYWORDS = [
    "系统升级", "系统维护", "技术调整", "规则修订", "服务器迁移", "证书更新", "网络调整",
    "接口变更", "交易时间调整", "交易日历变更", "参数修改", "IP变更", "维护通知"
]

def format_date(date_str: str) -> str:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d", "%Y-%m-%d %H:%M:%S"):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y/%m/%d")
        except Exception:
            continue
    return date_str

def mark_sensitive(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    for item in data:
        content = item.get("title", "") + item.get("link", "")
        item["sensitive"] = any(kw in content for kw in SENSITIVE_KEYWORDS)
    return data

def format_feishu_message(data: Dict[str, List[Dict]], filter_name: str) -> str:

    has_ann = [k for k,v in data.items() if len(v) > 0]
    no_ann = [k for k,v in data.items() if len(v) == 0]

    tz = pytz.timezone("Asia/Shanghai")
    currenttime = datetime.now(tz).strftime("%Y/%m/%d %H:%M")
    msg = f"期货交易所{filter_name}：[{currenttime}]\n\n"

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
        msg += f"\n以下是{ex}截至{currenttime}的{filter_name}：\n"

        for i, ann in enumerate(ann_list, 1):
            title = ann["title"]
            link = ann["link"]
            date = format_date(ann["date"])

            if ann.get("sensitive"):
                title = f"**[敏感]** {title}"

            msg += f"{i}. [{title}]({link}) 时间：{date}\n"

    return msg
