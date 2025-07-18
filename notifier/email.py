import smtplib
from email.mime.text import MIMEText
from email.header import Header
from typing import List

class EmailNotifier:
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str, sender: str, receivers: List[str]):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender = sender
        self.receivers = receivers

    def send_email(self, subject: str, content: str):
        try:
            message = MIMEText(content, 'plain', 'utf-8')
            message['From'] = self.sender
            message['To'] = ", ".join(self.receivers)
            message['Subject'] = Header(subject, 'utf-8')

            if self.smtp_port == 465:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as smtp:
                    smtp.login(self.username, self.password)
                    smtp.sendmail(self.sender, self.receivers, message.as_string())
                    smtp.quit()
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(self.username, self.password)
                    smtp.sendmail(self.sender, self.receivers, message.as_string())
                    smtp.quit()
        except Exception as e:
            print(f'[Email send error] {type(e).__name__}: {e}')