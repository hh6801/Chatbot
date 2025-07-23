import requests
import json
import os
import re
from bs4 import BeautifulSoup

# Constants
BASE_URL = "https://support.optisigns.com/api/v2/help_center/en-us"
HEADERS = {"Content-Type": "application/json"}
OUTPUT_DIR = "markdown_articles"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_all(endpoint):
    """Fetch all paginated data from Zendesk API."""
    results = []
    url = f"{BASE_URL}/{endpoint}.json"
    while url:
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error {res.status_code} when calling {url}")
            print(res.text)
            break
        data = res.json()
        key = endpoint.split("/")[-1]
        results.extend(data.get(key, []))
        url = data.get("next_page")
    return results

def slugify(text):
    """Generate a filename-safe slug."""
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')[:60]

def make_unique_filename(slug):
    """Ensure no filename conflict by appending suffix."""
    filename = f"{slug}.md"
    i = 1
    while os.path.exists(os.path.join(OUTPUT_DIR, filename)):
        filename = f"{slug}-{i}.md"
        i += 1
    return filename

def html_to_markdown(html):
    """Clean HTML and convert to markdown-like text."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove unnecessary tags
    for tag in soup(['nav', 'footer', 'header', 'script', 'style']):
        tag.decompose()

    # Format code
    for pre in soup.find_all('pre'):
        code_text = pre.get_text()
        pre.replace_with(f"\n```\n{code_text}\n```\n")

    # Format inline code
    for code in soup.find_all('code'):
        code.replace_with(f"`{code.get_text()}`")

    # Format headings
    for h in soup.find_all(['h1', 'h2', 'h3']):
        level = int(h.name[1])
        h.insert_before('\n' + '#' * level + f" {h.get_text()}\n")
        h.decompose()

    text = soup.get_text(separator="\n", strip=True)
    text = re.sub(r'\n{3,}', '\n\n', text)  # reduce multiple newlines
    return text

def scrape_and_save(limit=100):
    print("Fetching articles...")
    articles = get_all("articles")
    print("Fetching sections...")
    sections = get_all("sections")
    print("Fetching categories...")
    categories = get_all("categories")

    section_map = {s["id"]: s for s in sections}
    category_map = {c["id"]: c for c in categories}

    count = 0
    for article in articles:
        if article.get("draft") or article.get("locale") != "en-us":
            continue

        article_id = str(article["id"])
        title = article["title"]
        slug = slugify(title)
        filename = f"{article_id}_{slug}.md"  
        filepath = os.path.join(OUTPUT_DIR, filename)

        body = html_to_markdown(article.get("body", ""))
        url = article.get("html_url", "")
        updated = article.get("updated_at", "")
        section_name = section_map.get(article["section_id"], {}).get("name", "")
        category_id = section_map.get(article["section_id"], {}).get("category_id")
        category_name = category_map.get(category_id, {}).get("name", "")

        content = f"# {title}\n\n"
        content += f"- Category: {category_name}\n"
        content += f"- Section: {section_name}\n"
        content += f"- Last Updated: {updated}\n"
        content += f"- Articles URL: [{url}]({url})\n\n"
        content += "---\n\n"
        content += body
        content += f"\n\n---\n\n[View Article]({url})"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        count += 1
        print(f"Saved: {filename}")
        if count >= limit:
            break

    print(f"\n Total {count} articles saved in `{OUTPUT_DIR}`.")


if __name__ == "__main__":
    scrape_and_save()
