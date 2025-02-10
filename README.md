# Broken Link Checker

A Python-based web crawler that checks for broken links on websites. It handles Cloudflare-protected sites and can output results in multiple formats.

## Features

- Recursively crawls websites to find broken links
- Handles Cloudflare-protected websites using `cloudscraper`
- Ignores Cloudflare email protection links to reduce false positives
- Multiple output formats (Text, CSV, JSON)
- Stays within the same domain during crawling

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python broken_link_checker.py URL [--format {text|csv|json}]
```

### Parameters

- `URL`: The starting URL to crawl (required)
- `--format`: Output format (optional, defaults to text)
  - `text`: Human-readable format
  - `csv`: Comma-separated values
  - `json`: JSON structure

### Examples

1. Basic usage with text output:
```bash
python broken_link_checker.py https://example.com
```

2. CSV output format:
```bash
python broken_link_checker.py https://example.com --format csv
```

3. JSON output format:
```bash
python broken_link_checker.py https://example.com --format json
```

### Output Format Examples

#### Text Format (Default)
```
Broken links found:

On page: https://example.com
  https://example.com/broken-link -> 404
  https://example.com/another-broken -> 500
```

#### CSV Format
```csv
Page,Broken Link,Status
https://example.com,https://example.com/broken-link,404
https://example.com,https://example.com/another-broken,500
```

#### JSON Format
```json
{
  "broken_links": [
    {
      "page": "https://example.com",
      "broken_links": [
        {
          "url": "https://example.com/broken-link",
          "status": 404
        },
        {
          "url": "https://example.com/another-broken",
          "status": 500
        }
      ]
    }
  ]
}
```

## Docker Usage

You can run the link checker using Docker. First, build the image:

```bash
docker build -t broken-link-checker .
```

Then run the container with your desired URL and options:

```bash
# Basic usage with text output
docker run broken-link-checker https://example.com

# Using CSV output format
docker run broken-link-checker https://example.com --format csv

# Using JSON output format
docker run broken-link-checker https://example.com --format json

# Save output to a file on your host machine
docker run broken-link-checker https://example.com --format json > results.json
```

## Note

The script automatically ignores:
- JavaScript links (starting with `javascript:`)
- Email links (starting with `mailto:`)
- Cloudflare email protection links
- Cloudflare email protection documentation pages