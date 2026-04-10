#!/usr/bin/env python3
"""
Scan Xiaohongshu for last-48h learning/desk-share posts and output top titles.
Requires manual login if the site prompts for it.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from playwright.sync_api import Playwright, sync_playwright


KEYWORDS_DEFAULT = ["学习书桌", "书桌分享", "桌面布置", "自习桌", "学习日常"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan XHS for hot titles in last 48h.")
    parser.add_argument("--keywords", nargs="+", default=KEYWORDS_DEFAULT)
    parser.add_argument("--max-items", type=int, default=200)
    parser.add_argument("--out", type=Path, default=Path("xhs_trend_scan.csv"))
    parser.add_argument("--headless", action="store_true", help="Run browser headless.")
    parser.add_argument(
        "--login-wait",
        type=int,
        default=60,
        help="Seconds to wait for manual login in the opened browser (0 to skip).",
    )
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dump-html", type=Path, default=None)
    parser.add_argument("--dump-state", type=Path, default=None)
    parser.add_argument("--screenshot", type=Path, default=None)
    return parser.parse_args()


def normalize_count(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    if "万" in text:
        return int(float(text.replace("万", "")) * 10000)
    if "k" in text.lower():
        return int(float(text.lower().replace("k", "")) * 1000)
    text = re.sub(r"[^\d]", "", text)
    return int(text) if text else 0


def parse_time(text: str, now: datetime) -> Optional[datetime]:
    text = text.strip()
    if not text:
        return None
    if "刚刚" in text:
        return now
    match = re.search(r"(\d+)\s*分钟前", text)
    if match:
        return now - timedelta(minutes=int(match.group(1)))
    match = re.search(r"(\d+)\s*小时前", text)
    if match:
        return now - timedelta(hours=int(match.group(1)))
    match = re.search(r"(\d+)\s*天前", text)
    if match:
        return now - timedelta(days=int(match.group(1)))
    match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if match:
        return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)), tzinfo=now.tzinfo)
    return None


def split_author_time(text: str) -> Dict[str, str]:
    parts = [p.strip() for p in text.splitlines() if p.strip()]
    if not parts:
        return {"author": "", "publish_text": ""}
    if len(parts) == 1:
        return {"author": parts[0], "publish_text": ""}
    return {"author": parts[0], "publish_text": parts[1]}


def collect_cards(page, now: datetime) -> List[Dict[str, Any]]:
    selectors = [
        "section.note-item",
        "div.note-item",
        "div.note-card",
        "section[class*='note']",
        "div[class*='note']",
        "section[class*='card']",
        "div[class*='card']",
    ]
    cards = []
    for selector in selectors:
        cards.extend(page.query_selector_all(selector))
    results: List[Dict[str, Any]] = []
    for card in cards:
        title_el = card.query_selector("[class*='title'], [class*='desc'], [class*='text'], h3")
        author_el = card.query_selector("[class*='name'], [class*='author']")
        time_el = card.query_selector("[class*='time']")
        like_el = card.query_selector("[class*='like']")
        collect_el = card.query_selector("[class*='collect']")
        comment_el = card.query_selector("[class*='comment']")
        link_el = card.query_selector("a")

        title = title_el.inner_text().strip() if title_el else ""
        author = author_el.inner_text().strip() if author_el else ""
        publish_text = time_el.inner_text().strip() if time_el else ""
        if author and not publish_text and "\n" in author:
            parsed = split_author_time(author)
            author = parsed["author"]
            publish_text = parsed["publish_text"]
        if author and publish_text and author == publish_text and "\n" in author:
            parsed = split_author_time(author)
            author = parsed["author"]
            publish_text = parsed["publish_text"]
        publish_time = parse_time(publish_text, now)
        like = normalize_count(like_el.inner_text()) if like_el else 0
        collect = normalize_count(collect_el.inner_text()) if collect_el else 0
        comment = normalize_count(comment_el.inner_text()) if comment_el else 0
        url = link_el.get_attribute("href") if link_el else ""

        if not title:
            continue
        results.append(
            {
                "title": title,
                "author": author.replace("\n", " ").strip(),
                "publish_time": publish_time.isoformat() if publish_time else publish_text.replace("\n", " ").strip(),
                "like": like,
                "collect": collect,
                "comment": comment,
                "url": url,
            }
        )
    return results


def collect_from_links(page) -> List[Dict[str, Any]]:
    links = page.query_selector_all("a[href*='/explore/']")
    results: List[Dict[str, Any]] = []
    for link in links:
        title = link.inner_text().strip()
        url = link.get_attribute("href") or ""
        if title:
            results.append(
                {
                    "title": title,
                    "author": "",
                    "publish_time": "",
                    "like": 0,
                    "collect": 0,
                    "comment": 0,
                    "url": url,
                }
            )
    return results


def is_hot(item: Dict[str, Any]) -> bool:
    like = item.get("like", 0) or 0
    collect = item.get("collect", 0) or 0
    if like >= 1000:
        return True
    if like >= 300 and like > 0 and collect / like >= 0.2:
        return True
    return False


def run(playwright: Playwright, args: argparse.Namespace) -> List[Dict[str, Any]]:
    browser = playwright.chromium.launch(headless=args.headless)
    page = browser.new_page()
    page.goto("https://www.xiaohongshu.com/explore", wait_until="domcontentloaded")

    if args.login_wait > 0:
        print(f"Waiting {args.login_wait}s for manual login if needed...")
        page.wait_for_timeout(args.login_wait * 1000)

    all_items: List[Dict[str, Any]] = []
    now = datetime.now(timezone(timedelta(hours=8)))
    cutoff = now - timedelta(hours=48)

    for keyword in args.keywords:
        page.fill("input[type=search], input[placeholder*='搜索']", keyword)
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)

        for _ in range(10):
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(1500)
            items = collect_cards(page, now)
            if not items:
                items = collect_from_links(page)
            all_items.extend(items)
            if len(all_items) >= args.max_items:
                break

    if args.dump_state:
        try:
            state = page.evaluate("() => window.__INITIAL_STATE__ || window.__SSR_DATA__ || null")
            args.dump_state.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass
    if args.dump_html:
        try:
            args.dump_html.write_text(page.content(), encoding="utf-8")
        except Exception:
            pass
    if args.screenshot:
        try:
            page.screenshot(path=str(args.screenshot), full_page=True)
        except Exception:
            pass
    if args.debug:
        print(f"Final URL: {page.url}")

    browser.close()

    filtered = []
    for item in all_items:
        publish_time_raw = item.get("publish_time", "")
        publish_time = None
        if isinstance(publish_time_raw, str):
            try:
                publish_time = datetime.fromisoformat(publish_time_raw)
            except ValueError:
                publish_time = None
        if publish_time and publish_time < cutoff:
            continue
        filtered.append(item)

    deduped: Dict[str, Dict[str, Any]] = {}
    for item in filtered:
        key = item.get("url") or item.get("title")
        if not key:
            continue
        if key not in deduped:
            deduped[key] = item
    return list(deduped.values())


def main() -> int:
    args = parse_args()
    try:
        with sync_playwright() as playwright:
            items = run(playwright, args)
    except Exception as exc:
        print(f"Scan failed: {exc}", file=sys.stderr)
        return 1

    hot_items = [item for item in items if is_hot(item)]
    hot_items.sort(key=lambda x: (x.get("like", 0), x.get("collect", 0)), reverse=True)
    top_items = hot_items[:10]

    with args.out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(top_items[0].keys()) if top_items else [])
        if top_items:
            writer.writeheader()
            writer.writerows(top_items)

    if not top_items:
        print("[]")
    else:
        print(json.dumps(top_items, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
