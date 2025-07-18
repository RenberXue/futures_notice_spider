
# Futures Notice Spider

This project is a Python-based web crawler that uses Playwright to scrape daily announcements from four Chinese futures exchanges:

- Dalian Commodity Exchange (DCE)
- Zhengzhou Commodity Exchange (CZCE)
- Shanghai Futures Exchange (SHFE)
- China Financial Futures Exchange (CFFEX)

## Features

- Fetch announcements' title, URL, and date from each exchange website
- Supports retry on failed crawling (`safe_crawl`).
- Filtering announcements by:
  - Daily announcements
  - Announcements from the past 3 days
  - Latest 5 announcements
- Sends filtered reports via Feishu Bot or email
- Configurable via environment variables (support `.env` files)
- Scheduled daily execution using GitHub Actions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/RenberXue/futures-notice-spider.git
   cd futures-notice-spider
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:

   ```bash
   playwright install
   ```

4. Create a `.env` file with your configuration (see `.env.example`).

## Usage

Run the spider manually:

```bash
python main.py
```

## Configuration

Configure the following environment variables in your `.env` file:

- `FEISHU_WEBHOOK`: Your Feishu bot webhook URL
- `FILTER_MODE`: Filter mode (`daily`, `3days`, or `latest10`)
- `SMTP_HOST`: SMTP server host for email sending
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASS`: SMTP password
- `EMAIL_SENDER`: Sender email address
- `EMAIL_RECEIVERS`: Receiver email addresses (comma separated)

## Scheduling

This project includes a GitHub Actions workflow to run daily at 20:00 (8 PM) Beijing time and send notifications automatically.
