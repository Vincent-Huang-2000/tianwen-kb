#!/usr/bin/env python3
"""
Rebuild entity_data.js from chapter HTML annotations.
V2: Extract clean context by stripping HTML first, then finding entity positions.
"""
import re, json, os, html as html_mod
from collections import defaultdict
from pathlib import Path
from html import unescape as html_unescape

CHAPTERS_DIR = Path(r"D:\24history\twz\tianwen-kb\docs\chapters")
OUTPUT = Path(r"D:\24history\twz\tianwen-kb\docs\kg\entity_data.js")

FILENAME_TO_BOOK = {
    "01_史记_天官书第五.html": "史记·天官书",
    "02_汉书_天文志.html": "汉书·天文志",
    "03_后汉书_天文志.html": "后汉书·天文志",
    "04_晋书_天文志.html": "晋书·天文志",
    "05_宋书_天文志.html": "宋书·天文志",
    "06_南齐书_天文志.html": "南齐书·天文志",
    "07_魏书_天象志.html": "魏书·天象志",
    "08_隋书_天文志.html": "隋书·天文志",
    "09_旧唐书_天文志.html": "旧唐书·天文志",
    "10_新唐书_天文志.html": "新唐书·天文志",
    "11_旧五代史_天文志.html": "旧五代史·天文志",
    "12_新五代史_司天考.html": "新五代史·司天考",
    "13_宋史_天文志.html": "宋史·天文志",
    "14_辽史_历象志.html": "辽史·历象志",
    "15_金史_天文志.html": "金史·天文志",
    "16_元史_天文志.html": "元史·天文志",
    "17_明史_天文志.html": "明史·天文志",
    "18_步天歌.html": "步天歌",
    "19_乙巳占.html": "乙巳占",
    "20_星庐中国古天文学概论.html": "星庐·中国古天文学概论",
}

TYPE_MAP = {
    "星": "恒星", "官": "星官", "曜": "行星", "象": "天象",
    "神": "神祇", "州": "州县", "岁": "纪年", "器": "仪器", "历": "历法"
}

CONTEXT_CHARS = 50  # chars before and after entity
MAX_CONTEXTS_PER_ENTITY = 5  # max context excerpts per entity


def strip_html(text):
    """Remove all HTML tags and decode entities."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = html_unescape(text)
    # Collapse whitespace
    text = re.sub(r'\s+', '', text)
    return text


def extract_body_text(html_content):
    """Extract and strip text from the chapter-body div only."""
    m = re.search(r'<div class="chapter-body[^"]*">(.*?)</main>', html_content, re.DOTALL)
    if not m:
        # Try alternative: chapter-body until closing div (with nesting)
        start = html_content.find('class="chapter-body')
        if start == -1:
            return strip_html(html_content)
        # Find the div opening
        div_start = html_content.rfind('<div', 0, start) if html_content.rfind('<div', 0, start) != -1 else start
        # Count nesting to find matching </div>
        depth = 1
        pos = html_content.find('>', start) + 1
        while depth > 0 and pos < len(html_content):
            next_open = html_content.find('<div', pos)
            next_close = html_content.find('</div>', pos)
            if next_close == -1:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    body_html = html_content[div_start : next_close + 6]
                    return strip_html(body_html)
                pos = next_close + 6
        return strip_html(html_content)
    
    body_html = m.group(1)
    return strip_html(body_html)


def find_entity_contexts(body_text, entity_name, max_contexts=None):
    """Find all occurrences of entity_name in body_text and return contexts."""
    contexts = []
    pos = 0
    name_len = len(entity_name)
    
    while True:
        idx = body_text.find(entity_name, pos)
        if idx == -1:
            break
        
        start = max(0, idx - CONTEXT_CHARS)
        end = min(len(body_text), idx + name_len + CONTEXT_CHARS)
        snippet = body_text[start:end]
        
        # Add ellipsis if truncated
        if start > 0:
            snippet = '…' + snippet
        if end < len(body_text):
            snippet = snippet + '…'
        
        contexts.append(snippet)
        pos = idx + name_len
        
        if max_contexts and len(contexts) >= max_contexts:
            break
    
    return contexts


# Parse all chapters
print("Parsing chapter HTML files...")
entity_contexts = defaultdict(list)

for html_file in sorted(CHAPTERS_DIR.glob("*.html")):
    fname = html_file.name
    if fname not in FILENAME_TO_BOOK:
        print(f"  SKIP: {fname} (no mapping)")
        continue
    
    book_name = FILENAME_TO_BOOK[fname]
    print(f"  Processing: {fname} → {book_name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract clean body text
    body_text = extract_body_text(content)
    
    # Find all entity spans and match them to body_text positions
    span_pattern = re.compile(
        r'<span\s+class="ent\s+ent-([^"]+)"\s+title="([^：<]+)：([^"]+)"[^>]*?>(.*?)</span>',
        re.DOTALL
    )
    
    # Extract entities: type, type_cn, name, display_text
    entities_found = []
    for m in span_pattern.finditer(content):
        ent_type_short = m.group(1)
        type_cn = m.group(2)
        ent_name = m.group(3)
        display_text = m.group(4)
        entities_found.append((ent_type_short, type_cn, ent_name, display_text))
    
    # Match each entity occurrence in body_text
    # Use a sliding window approach: for each entity name, find ALL occurrences in body_text
    # Then assign sequential numbers
    
    # Group entities by name
    name_occurrences = defaultdict(list)
    for ent_type_short, type_cn, ent_name, display_text in entities_found:
        name_occurrences[ent_name].append((ent_type_short, type_cn))
    
    # For each unique entity name in this chapter, get contexts
    seen_names = set()
    for ent_type_short, type_cn, ent_name, display_text in entities_found:
        if ent_name in seen_names:
            continue
        seen_names.add(ent_name)
        
        contexts = find_entity_contexts(body_text, ent_name, max_contexts=MAX_CONTEXTS_PER_ENTITY)
        
        for ctx_text in contexts[:MAX_CONTEXTS_PER_ENTITY]:
            entity_contexts[ent_name].append({
                "book": book_name,
                "type": ent_type_short,
                "type_cn": type_cn,
                "text": ctx_text,
            })

print(f"\nTotal unique entities: {len(entity_contexts)}")
total_occurrences = sum(len(v) for v in entity_contexts.values())
print(f"Total occurrences: {total_occurrences}")

# Build entity data
entities = []
for name, contexts_list in sorted(entity_contexts.items()):
    # Determine dominant type
    type_counts = defaultdict(int)
    for c in contexts_list:
        type_counts[(c["type"], c["type_cn"])] += 1
    dominant_type, dominant_type_cn = max(type_counts, key=type_counts.get)
    
    # Count per book
    book_counts = defaultdict(int)
    for c in contexts_list:
        book_counts[c["book"]] += 1
    
    # Sort contexts: group by book, preserve order
    numbered_contexts = []
    for i, c in enumerate(contexts_list, 1):
        numbered_contexts.append({
            "seq": i,
            "text": c["text"],
            "book": c["book"],
        })
    
    entities.append({
        "name": name,
        "type": dominant_type,
        "type_cn": dominant_type_cn,
        "total": len(contexts_list),
        "books": dict(sorted(book_counts.items(), key=lambda x: -x[1])),
        "book_count": len(book_counts),
        "contexts": numbered_contexts,
    })

# Sort entities by total occurrences desc
entities.sort(key=lambda e: -e["total"])

# Build BOOK_URLS
book_urls = {}
for fname, book in FILENAME_TO_BOOK.items():
    book_urls[book] = f"../chapters/{fname}"

# Generate JS output
js_lines = [
    f"window.ENTITIES={json.dumps(entities, ensure_ascii=False, separators=(',', ':'))};",
    f"window.BOOK_URLS={json.dumps(book_urls, ensure_ascii=False, separators=(',', ':'))};"
]

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

print(f"\nWritten to: {OUTPUT}")
print(f"Entities: {len(entities)}")
print(f"Total contexts: {sum(e['total'] for e in entities)}")

# Summary
print("\n=== Type Summary ===")
type_summary = defaultdict(lambda: {"count": 0, "total": 0})
for e in entities:
    t = e["type_cn"]
    type_summary[t]["count"] += 1
    type_summary[t]["total"] += e["total"]

for t in ["恒星", "星官", "行星", "天象", "神祇", "州县", "纪年", "仪器", "历法"]:
    if t in type_summary:
        s = type_summary[t]
        print(f"  {t}: {s['count']} entities, {s['total']} occurrences")

print("\n=== Top 15 Entities ===")
for i, e in enumerate(entities[:15], 1):
    books_str = "、".join(list(e['books'].keys())[:3])
    if len(e['books']) > 3:
        books_str += f"等{e['book_count']}部"
    print(f"  {i:>2}. {e['name']} [{e['type_cn']}] {e['total']}次 {books_str}")
