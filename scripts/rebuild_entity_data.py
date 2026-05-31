#!/usr/bin/env python3
"""
Rebuild entity_data.js from chapter HTML annotations.
Extracts ALL entity spans, captures surrounding context, groups by entity name.
Assigns sequential numbers, preserves book mapping.
"""
import re, json, os, html as html_mod
from collections import defaultdict
from pathlib import Path

CHAPTERS_DIR = Path(r"D:\24history\twz\tianwen-kb\docs\chapters")
OUTPUT = Path(r"D:\24history\twz\tianwen-kb\docs\kg\entity_data.js")

# Filename → display name mapping (derived from existing BOOK_URLS)
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

CONTEXT_CHARS = 80  # chars before and after entity for context snippet

def strip_html(text):
    """Remove HTML tags, keep text content."""
    return re.sub(r'<[^>]+>', '', text)

def extract_text_context(html_content, start_pos, end_pos):
    """Extract text context around a position in HTML."""
    # Take surrounding raw text, then strip tags
    raw_before = html_content[max(0, start_pos - 500):start_pos]
    raw_after = html_content[end_pos:end_pos + 500]
    
    # Get text-only versions
    text_before = strip_html(raw_before)
    text_after = strip_html(raw_after)
    
    # Take last CONTEXT_CHARS chars of before, first CONTEXT_CHARS of after
    context_before = text_before[-CONTEXT_CHARS:] if len(text_before) > CONTEXT_CHARS else text_before
    context_after = text_after[:CONTEXT_CHARS] if len(text_after) > CONTEXT_CHARS else text_after
    
    return (context_before + "…" + context_after).strip()

def clean_context(text):
    """Clean up context text."""
    text = re.sub(r'\s+', '', text)
    text = html_mod.unescape(text)
    return text

# Parse all chapters
print("Parsing chapter HTML files...")
entity_contexts = defaultdict(list)  # entity_name -> list of context dicts

for html_file in sorted(CHAPTERS_DIR.glob("*.html")):
    fname = html_file.name
    if fname not in FILENAME_TO_BOOK:
        print(f"  SKIP: {fname} (no mapping)")
        continue
    
    book_name = FILENAME_TO_BOOK[fname]
    print(f"  Processing: {fname} → {book_name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all entity spans
    # Pattern: <span class="ent ent-{type}" title="{type_cn}：{name}" style="..." onclick="...">text</span>
    span_pattern = re.compile(
        r'<span\s+class="ent\s+ent-([^"]+)"\s+title="([^：]+)：([^"]+)"[^>]*onclick="[^"]*name=([^&]+)&ref=([^"]+)"[^>]*>(.*?)</span>',
        re.DOTALL
    )
    
    for m in span_pattern.finditer(content):
        ent_type_short = m.group(1)   # e.g., "神"
        type_cn = m.group(2)           # e.g., "神祇"
        ent_name = m.group(3)          # e.g., "天一"
        url_name = m.group(4)          # e.g., "%E5%A4%A9%E4%B8%80"
        ref_file = m.group(5)          # e.g., "01_史记_天官书第五.html"
        display_text = m.group(6)      # text between span tags
        
        # Decode URL-encoded name
        from urllib.parse import unquote
        decoded_name = unquote(url_name)
        
        # Extract context
        context_snippet = extract_text_context(content, m.start(), m.end())
        context_snippet = clean_context(context_snippet)
        
        entity_contexts[decoded_name].append({
            "book": book_name,
            "type": ent_type_short,
            "type_cn": type_cn,
            "text": context_snippet,
            "ref": ref_file,
        })

print(f"\nTotal unique entities: {len(entity_contexts)}")
total_occurrences = sum(len(v) for v in entity_contexts.values())
print(f"Total occurrences: {total_occurrences}")

# Build entity data
entities = []
for name, contexts in sorted(entity_contexts.items()):
    # Determine dominant type
    type_counts = defaultdict(int)
    for c in contexts:
        type_counts[(c["type"], c["type_cn"])] += 1
    dominant_type, dominant_type_cn = max(type_counts, key=type_counts.get)
    
    # Count per book
    book_counts = defaultdict(int)
    for c in contexts:
        book_counts[c["book"]] += 1
    
    # Sort contexts: first by book, then preserve within-book order
    # Assign sequential numbers
    numbered_contexts = []
    for i, c in enumerate(contexts, 1):
        numbered_contexts.append({
            "seq": i,
            "text": c["text"],
            "book": c["book"],
        })
    
    entities.append({
        "name": name,
        "type": dominant_type,
        "type_cn": dominant_type_cn,
        "total": len(contexts),
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
js_lines = []
js_lines.append(f"window.ENTITIES={json.dumps(entities, ensure_ascii=False, separators=(',', ':'))};")
js_lines.append(f"window.BOOK_URLS={json.dumps(book_urls, ensure_ascii=False, separators=(',', ':'))};")

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(js_lines))

print(f"\nWritten to: {OUTPUT}")
print(f"Entities: {len(entities)}")
print(f"Total contexts: {sum(e['total'] for e in entities)}")

# Print summary
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
