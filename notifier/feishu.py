import requests
import json

class FeishuNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_message(self, text: str):
        try:
            headers = {"Content-Type": "application/json"}
            payload = {
                "msg_type": "text",
                "content": {
                    "text": text
                }
            }
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
        except Exception as e:
            print(f'[Feishu send error] {type(e).__name__}: {e}')