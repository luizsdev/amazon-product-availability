# Amazon Product Availability Checker

This script monitors the availability of a product on Amazon and sends an email notification when the product becomes available.

## Prerequisites

- Python 3.x
- Chrome browser
- ChromeDriver

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your configuration:
- Set your Amazon product URL
- Configure your email settings
- Adjust search text and check interval as needed

## Email Setup

To use Gmail SMTP:
1. Enable 2-factor authentication in your Google Account
2. Generate an App Password for this application
3. Use the App Password in the `SENDER_PASSWORD` environment variable

## Usage

Run the script:
```bash
python3 check-product-availability.py
```

The script will:
1. Check the product availability every X seconds
2. Send an email notification when the product becomes available
3. Exit after sending the notification

## Environment Variables

- `AMAZON_URL`: The Amazon product URL to monitor
- `SMTP_SERVER`: SMTP server address (default: smtp.gmail.com)
- `SMTP_PORT`: SMTP server port (default: 587)
- `SENDER_EMAIL`: Your Gmail address
- `SENDER_PASSWORD`: Your Gmail App Password
- `RECIPIENT_EMAIL`: Email address to receive notifications
- `PRODUCT_NAME`: Product name (default: Product)
- `CHROME_DRIVER_PATH`: Path of the chrome driver executable (default: /usr/bin/chromedriver)
- `SEARCH_TEXT`: Text to search for to determine availability (default : Currently unavailable.)
- `CHECK_INTERVAL_SECONDS`: Base interval between checks (default: 30)
