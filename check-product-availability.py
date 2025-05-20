from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import os
from dotenv import load_dotenv

load_dotenv()

AMAZON_URL = os.getenv('AMAZON_URL')
CHECK_INTERVAL_SECONDS = int(os.getenv('CHECK_INTERVAL_SECONDS', '30'))
SEARCH_TEXT = os.getenv('SEARCH_TEXT', 'Currently unavailable.')

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
PRODUCT_NAME = os.getenv('PRODUCT_NAME', 'Product')

required_vars = ['AMAZON_URL', 'SENDER_EMAIL', 'SENDER_PASSWORD', 'RECIPIENT_EMAIL']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def get_html_with_selenium(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.3')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-first-run')
    options.add_argument('--single-process')

    chrome_driver_path = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    chrome_service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=options)
    try:
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        return html
    finally:
        driver.quit()

def check_availability():
    try:
        html = get_html_with_selenium(AMAZON_URL)
        soup = BeautifulSoup(html, 'html.parser')
        found = SEARCH_TEXT in soup.text
        print(f"Search text '{SEARCH_TEXT}' found: {found}")
        if found:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error fetching page: {e}")
        import traceback
        traceback.print_exc()
        return False

def send_email():
    subject = f"{PRODUCT_NAME} is available!"
    body = f"The product is now available: {AMAZON_URL}"
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("Starting Amazon product availability checker...")
    while True:
        available = check_availability()
        if available:
            print(f"{PRODUCT_NAME} is available! Sending email...")
            send_email()
            break
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Not available yet. Checking again in {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
