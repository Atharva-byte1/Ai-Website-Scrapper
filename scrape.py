from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

def scrape_website(url, max_pages=3):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service("./chromedriver.exe"),
        options=options
    )

    visited = set()
    to_visit = [url]
    all_text_lines = []

    try:
        while to_visit and len(visited) < max_pages:
            current_url = to_visit.pop(0)

            if current_url in visited:
                continue

            visited.add(current_url)

            driver.get(current_url)
            time.sleep(4)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # remove non-visible content
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n")
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            all_text_lines.extend(lines)

            # collect internal links
            base_domain = urlparse(url).netloc
            for a in soup.find_all("a", href=True):
                full_url = urljoin(current_url, a["href"])
                if urlparse(full_url).netloc == base_domain:
                    if full_url not in visited and full_url not in to_visit:
                        to_visit.append(full_url)

    finally:
        driver.quit()

    return all_text_lines
