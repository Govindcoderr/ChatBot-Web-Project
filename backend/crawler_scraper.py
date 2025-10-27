# from playwright.sync_api import sync_playwright
# from bs4 import BeautifulSoup
# import re
# from urllib.parse import urljoin, urlparse
# import time

# def same_domain(base_url, link):
#     return urlparse(base_url).netloc == urlparse(link).netloc

# def clean_page_text(soup):
#     for tag in soup(["script", "style", "noscript", "svg", "img", "button"]):
#         tag.decompose()
#     text = soup.get_text(separator="\n")
#     text = re.sub(r'\n+', '\n', text)
#     text = re.sub(r'\s+', ' ', text).strip()
#     return text

# def fetch_rendered_html(url):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (compatible; GovindBot/1.0)"})
#         page.goto(url, timeout=90000)
#         page.wait_for_load_state("networkidle")
#         html = page.content()
#         # Include iframe content if needed
#         for frame in page.frames:
#             try:
#                 html += frame.content()
#             except:
#                 pass
#         browser.close()
#         return html

# def crawl_and_scrape(base_url, max_pages=10, delay=1):
#     visited = set()
#     to_visit = [base_url]
#     all_texts = []

#     print(f"🚀 Starting crawl: {base_url}")

#     while to_visit and len(visited) < max_pages:
#         url = to_visit.pop(0)
#         if url in visited:
#             continue
#         try:
#             html = fetch_rendered_html(url)
#             soup = BeautifulSoup(html, "html.parser")
#             text = clean_page_text(soup)

#             if text and len(text.split()) > 20:
#                 formatted_text = f"----- PAGE: {url} -----\n\n{text}"
#                 all_texts.append(formatted_text)
#                 print(f"✅ Crawled: {url}")
#             else:
#                 print(f"⚠️ Skipped (too little text): {url}")

#             visited.add(url)

#             # Queue internal links
#             for link_tag in soup.find_all("a", href=True):
#                 link = urljoin(base_url, link_tag["href"])
#                 if same_domain(base_url, link) and link not in visited:
#                     to_visit.append(link)

#             time.sleep(delay)
#         except Exception as e:
#             print(f"⚠️ Error visiting {url}: {e}")
#             continue

#     if not all_texts:
#         print("⚠️ No valid content scraped. Try another site.")
#     else:
#         print(f"\n✅ Finished crawling {len(visited)} pages.")

#     return all_texts




import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def same_domain(base_url, link):
    return urlparse(base_url).netloc == urlparse(link).netloc

def clean_text(soup):
    """Remove scripts, styles, headers, footers, etc."""
    for tag in soup(["script", "style", "noscript", "header", "footer", "svg", "img", "button", "aside", "form", "nav"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

async def fetch(session, url):
    """Fetch a page asynchronously with headers."""
    try:
        async with session.get(url, timeout=15) as response:
            if response.status != 200:
                return None
            html = await response.text()
            return html
    except:
        return None

async def crawl_page(session, url, base_url, visited, to_visit, all_texts, min_words=20):
    if url in visited:
        return
    visited.add(url)

    html = await fetch(session, url)
    if not html:
        return

    soup = BeautifulSoup(html, "html.parser")
    text = clean_text(soup)

    if len(text.split()) >= min_words:
        formatted_text = f"----- PAGE: {url} -----\n\n{text}"
        all_texts.append(formatted_text)
        print(f"✅ Crawled: {url}")
    else:
        print(f"⚠️ Skipped (too little text): {url}")

    # Queue internal links
    for link_tag in soup.find_all("a", href=True):
        link = urljoin(base_url, link_tag["href"])
        if same_domain(base_url, link) and link not in visited:
            to_visit.append(link)

async def crawl_and_scrape(base_url, max_pages=10):
    """Async crawler for multiple pages."""
    visited = set()
    to_visit = [base_url]
    all_texts = []

    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0 (compatible; GovindBot/1.0)"}) as session:
        while to_visit and len(visited) < max_pages:
            # Fetch pages concurrently
            tasks = []
            for _ in range(min(len(to_visit), max_pages - len(visited))):
                url = to_visit.pop(0)
                tasks.append(crawl_page(session, url, base_url, visited, to_visit, all_texts))
            await asyncio.gather(*tasks)

    print(f"\n✅ Finished crawling {len(visited)} pages.")
    return all_texts

# # Example usage
# if __name__ == "__main__":
#     url = "https://www.moneycontrol.com/"
#     all_texts = asyncio.run(crawl_and_scrape(url, max_pages=5))

#     # Save to file
#     with open("crawled_content_fast.txt", "w", encoding="utf-8") as f:
#         f.write("\n\n".join(all_texts))
