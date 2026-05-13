#!/usr/bin/env python3
"""
Fetch Behance RSS for a given user and write a clean projects.json.

Stdlib only — runs on the GitHub Actions ubuntu-latest runner's pre-installed
Python without `pip install`. Designed to be re-runnable; only the contents
of projects.json change between runs.

The schema written to projects.json:

    {
      "username": "ryoticoalu",
      "fetched_at": "2026-05-14T04:00:00Z",
      "source": "https://www.behance.net/feeds/user?username=ryoticoalu",
      "projects": [
        {
          "id": "194326607",
          "title": "Portfolio - Motion Graphic Animation",
          "url": "https://www.behance.net/gallery/194326607/...",
          "thumbnail": "https://mir-s3-cdn-cf.behance.net/.../source.jpg",
          "published": "2024-03-20T00:00:00Z",
          "category": null
        },
        ...
      ]
    }

`category` is null by default. To tag projects, create a sibling
behance-categories.json mapping IDs to category strings; this script will
merge those tags into the output. See behance-categories.json (or its
absence — that's fine, projects are left untagged).
"""

import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

USERNAME = os.environ.get("BEHANCE_USERNAME", "ryoticoalu")
RSS_URL = f"https://www.behance.net/feeds/user?username={USERNAME}"
OUTPUT_PATH = pathlib.Path("projects.json")
CATEGORIES_PATH = pathlib.Path("behance-categories.json")

USER_AGENT = "Mozilla/5.0 (compatible; ryoticoalu-portfolio-sync/1.0; +https://github.com/ryoticoalu/ryoticoalu-portfolio)"


def fetch_rss(url: str) -> bytes:
    """Fetch the RSS body. Returns raw bytes (XML)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def extract_thumbnail_from_description(description: str) -> str | None:
    """Behance RSS embeds the thumbnail inside the <description> as an <img src>.
    Pull the first src= URL we see. Returns None if not found."""
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', description, re.IGNORECASE)
    return m.group(1) if m else None


def gallery_id_from_url(url: str) -> str | None:
    """https://www.behance.net/gallery/194326607/Some-Slug -> '194326607'"""
    m = re.search(r"/gallery/(\d+)/", url)
    return m.group(1) if m else None


def parse_pubdate(s: str) -> str:
    """RFC 822 (RSS) -> ISO 8601 UTC."""
    try:
        # Most RSS uses: "Wed, 20 Mar 2024 00:00:00 +0000"
        d = dt.datetime.strptime(s.strip(), "%a, %d %b %Y %H:%M:%S %z")
        return d.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    except ValueError:
        # Fallback: just return the raw string so we don't lose information.
        return s


def parse_feed(xml_bytes: bytes) -> list[dict]:
    """Parse the RSS XML into a list of project dicts."""
    root = ET.fromstring(xml_bytes)
    # Channel is root/channel; items are root/channel/item
    channel = root.find("channel")
    if channel is None:
        return []
    items = channel.findall("item")
    projects: list[dict] = []
    for it in items:
        title = (it.findtext("title") or "").strip()
        link = (it.findtext("link") or "").strip()
        description = it.findtext("description") or ""
        pubdate = it.findtext("pubDate") or ""
        gid = gallery_id_from_url(link)
        projects.append({
            "id": gid,
            "title": title,
            "url": link,
            "thumbnail": extract_thumbnail_from_description(description),
            "published": parse_pubdate(pubdate),
            "category": None,
        })
    return projects


def merge_categories(projects: list[dict], categories_path: pathlib.Path) -> list[dict]:
    """If behance-categories.json exists, set `category` for each matching project ID."""
    if not categories_path.exists():
        return projects
    try:
        mapping = json.loads(categories_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"WARN: {categories_path} is malformed: {e}. Skipping category merge.", file=sys.stderr)
        return projects
    for p in projects:
        gid = p.get("id")
        if gid and gid in mapping:
            p["category"] = mapping[gid]
    return projects


def main() -> int:
    print(f"Fetching Behance RSS for user '{USERNAME}'...")
    try:
        xml_bytes = fetch_rss(RSS_URL)
    except Exception as e:
        print(f"ERROR: failed to fetch RSS: {e}", file=sys.stderr)
        return 2

    projects = parse_feed(xml_bytes)
    print(f"Parsed {len(projects)} project(s) from feed.")

    projects = merge_categories(projects, CATEGORIES_PATH)

    output = {
        "username": USERNAME,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
        "source": RSS_URL,
        "projects": projects,
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} ({OUTPUT_PATH.stat().st_size} bytes).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
