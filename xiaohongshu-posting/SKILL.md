---
name: xiaohongshu-posting
description: Create Xiaohongshu (RED) post topics, titles, body copy, and tags from user-provided desk/study photos; iterate on copy with a human tone; optionally guide the user through web publishing after explicit confirmation.
---

# Xiaohongshu Posting

## Overview

Generate 1-3 sets of titles and body copy for late-night study desk posts with a warm,真实、生活感 tone, then iterate and optionally guide web posting.

## Workflow

### 0) (Optional) Trend scan: last 48h爆款标题（自动化）

- Ask whether to run a 48h trend scan for learning/desk-share posts.
- If yes, request explicit approval for networked browsing and any automation.
- Use `scripts/xhs_trend_scan_playwright.py` to search Xiaohongshu with keywords `学习书桌`, `书桌分享`, `桌面布置`, `自习桌`, `学习日常`.
- Default sort: newest; collect posts from the last 48 hours.
- Capture fields: `title`, `author`, `publish_time`, `like`, `collect`, `comment`, `url`.
- Define "爆款" using a simple rule: `like >= 1000` OR (`collect/like >= 0.2` AND `like >= 300`).
- Return top 10 titles with basic stats; ask the user which titles to emulate or avoid.
- If headless gets blocked or shows verification, rerun with a visible browser and manual login.
- Dependency: `pip install playwright` and `playwright install`.
- Run: `python skills/xiaohongshu-posting/scripts/xhs_trend_scan_playwright.py --out xhs_trend_scan.csv --login-wait 60`.

### 1) Intake and constraints

- Ask for the photo set if not already provided.
- Ask for optional details if missing: today's mood, study method used, time spent, any specific desk items to highlight.
- Confirm: user wants 1-3 title/body/tag sets and iterative edits.

### 2) Draft generation

- Produce 1-3 options, each with: title, body, tags.
- Use emojis but keep them restrained and context-fit.
- Body length target: roughly one phone screen, with blank lines between paragraphs.
- Ensure each body includes: a concrete method/detail + a short personal reflection/feeling.
- Avoid obvious AI tone, overused chicken-soup phrasing, and stiff templates.
- Default tags (adjust if needed): `#书桌日常 #学习日常 #桌面好物 #自我提升`.

### 3) Iterate

- Ask which option to keep and what to adjust (tone, method details, items, length).
- Provide revised versions until the user approves.

### 4) Publish (web flow, confirmation only)

- Ask: "是否需要我帮你网页端发布到小红书？"
- Only proceed after explicit confirmation.
- If confirmed, present a step-by-step web publishing checklist and ask the user to confirm login/permissions before any automated action.

## Output format

Use the following field separators exactly:

标题1：...
正文1：...
标签：#书桌日常 #学习日常 #桌面好物 #自我提升

标题2：...
正文2：...
标签：...

## Style guide (summary)

- Scene: 深夜学习氛围 + 书桌好物分享，胡桃木桌面、昏黄暖光、Mac/书本/生活小物。
- Value: "方法细节" + "情绪价值" must both be present.
- Language: 真实、生活感、不过度鸡汤，不夸张营销。
- Titles: rotate 2-3 skeletons (方法论+结果、场景+收获、反直觉+小突破) to keep variety.

## References

- Read `references/style-samples.md` when matching tone and rhythm.
- Read `references/project-notes.md` for current rules and scope decisions.
