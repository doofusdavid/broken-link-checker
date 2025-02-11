#!/usr/bin/env python3
import argparse
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
# Some good documentation

def is_valid_link(link):
    if not link:
        return False
    
    # Ignore javascript and mailto links
    if link.startswith("javascript:") or link.startswith("mailto:"):
        return False
        
    # Ignore Cloudflare email protection URLs
    if "/cdn-cgi/l/email-protection" in link:
        return False
    
    # Ignore Cloudflare email protection related documentation
    if "cloudflare.com" in link and any(x in link for x in [
        "email-protection",
        "email_protection",
        "What-is-Email-Address-Obfuscation"
    ]):
        return False
        
    return True

def check_link(scraper, url):
    try:
        r = scraper.get(url, timeout=10)
        if r.status_code >= 400:
            return False, r.status_code
        return True, r.status_code
    except Exception as e:
        return False, str(e)

def crawl(url, scraper, visited, broken_links, base_domain):
    if url in visited:
        return
    visited.add(url)
    print(f"Crawling: {url}")
    
    try:
        resp = scraper.get(url, timeout=10)
    except Exception as e:
        print(f"Failed to load {url}: {e}")
        return

    if resp.status_code >= 400:
        print(f"Skipping broken page: {url} ({resp.status_code})")
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    # Find all anchor tags with href
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if not is_valid_link(href):
            continue

        full_url = urljoin(url, href)
        # Check link status
        valid, status = check_link(scraper, full_url)
        if not valid:
            broken_links.setdefault(url, []).append((full_url, status))
        
        # Only crawl links within the same domain
        if urlparse(full_url).netloc.endswith(base_domain) and full_url not in visited:
            crawl(full_url, scraper, visited, broken_links, base_domain)

def output_text(broken_links):
    if broken_links:
        print("\nBroken links found:")
        for page, links in broken_links.items():
            print(f"\nOn page: {page}")
            for link, status in links:
                print(f"  {link} -> {status}")
    else:
        print("No broken links found.")

def output_csv(broken_links):
    import csv
    import sys
    writer = csv.writer(sys.stdout)
    writer.writerow(["Page", "Broken Link", "Status"])
    if broken_links:
        for page, links in broken_links.items():
            for link, status in links:
                writer.writerow([page, link, status])

def output_json(broken_links):
    import json
    output = {
        "broken_links": [
            {
                "page": page,
                "broken_links": [
                    {"url": link, "status": status}
                    for link, status in links
                ]
            }
            for page, links in broken_links.items()
        ]
    }
    print(json.dumps(output, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Broken Link Checker")
    parser.add_argument("url", help="Starting URL to crawl")
    parser.add_argument(
        "--format",
        choices=["text", "csv", "json"],
        default="text",
        help="Output format (default: text)"
    )
    args = parser.parse_args()

    starting_url = args.url
    base_domain = urlparse(starting_url).netloc
    scraper = cloudscraper.create_scraper()
    
    visited = set()
    broken_links = {}
    crawl(starting_url, scraper, visited, broken_links, base_domain)

    # Output in the selected format
    if args.format == "csv":
        output_csv(broken_links)
    elif args.format == "json":
        output_json(broken_links)
    else:  # text
        output_text(broken_links)

if __name__ == "__main__":
    main()
