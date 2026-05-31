#!/usr/bin/env python3
"""Generate body_html from markdown, then inject into backup #5 template.

This avoids the broken TOC conversion — use backup #5's proven CSS+JS shell,
replace only the chapter-body content."""
import re
from pathlib import Path

MD_PATH = Path(r"D:\24history\twz\星庐中国古天文学概论.md")
BACKUP5_PATH = Path(r"D:\24history\twz\tianwen-kb\docs\chapters\20_星庐中国古天文学概论.html")
OUTPUT_PATH = BACKUP5_PATH

# Step 1: Git restore and read backup #5 template
import subprocess
subprocess.run(['git', '-C', str(BACKUP5_PATH.parent.parent), 'checkout', '8b80c72', '--', 'docs/chapters/20_星庐中国古天文学概论.html'], capture_output=True)
print("Restored backup #5")

with open(BACKUP5_PATH, 'r', encoding='utf-8') as f:
    template = f.read()

# Step 3: Read markdown and convert to body HTML (simple line-by-line)
with open(MD_PATH, 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

TYPE_MAP = {'星':'恒星','官':'星官','曜':'行星','象':'天象','神':'神祇','州':'州县','岁':'纪年','器':'仪器','历':'历法'}
REF_FILE = '20_星庐中国古天文学概论.html'

def apply_entities(text):
    def repl(m):
        t, name = m.group(1), m.group(2)
        return f'<span class="ent ent-{t}" title="{TYPE_MAP.get(t,t)}：{name}" style="cursor:pointer" onclick="window.open(\'../kg/entity.html?name={name}&ref={REF_FILE}\',\'_blank\')">{name}</span>'
    return re.sub(r'\[(\S+) ([^\]]+)\]', repl, text)

def is_caption(line):
    s = re.sub(r'<a\s+id="[^"]*"></a>', '', line).strip()
    return bool(re.match(r'^(图\d+|图表\d+)$', s))

result = []
i = 0
in_toc = False
toc_items = []

while i < len(md_lines):
    line = md_lines[i].rstrip('\n')
    if not line.strip():
        i += 1; continue

    # Title/author bold lines
    if line.startswith('__') and '__' in line[2:]:
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', line)
        result.append(f'<p>{apply_entities(text)}</p>')
        i += 1; continue

    # TOC start
    if '目 录' in line:
        print(f'DEBUG: TOC start at i={i}')
        result.append('<p>目 录</p>')
        in_toc = True; i += 1; continue

    if in_toc:
        # TOC entry: [text\ttab](#anchor)
        m = re.match(r'\[(.+?)(?:\t\d+)?\]\((#_[^)]+)\)', line)
        if m:
            toc_text = m.group(1).replace('\\.', '.')
            if len(toc_items) == 0:
                print(f'TOC first match: text={repr(toc_text[:30])}')
            # Don't apply entities to TOC — just plain text links
            toc_items.append(f'<a href="{m.group(2)}">{toc_text}</a>')
            i += 1; continue
        elif line.startswith('#'):
            # TOC ends at next heading
            in_toc = False
            if toc_items:
                result.append('<p>\n' + '\n'.join(toc_items) + '\n</p>')
                toc_items = []
            # Fall through to process heading
        else:
            i += 1; continue

    # Image
    img_m = re.match(r'!\[\]\(([^)]+)\)', line)
    if img_m:
        result.append(f'<span class="img-ref" data-img="../{img_m.group(1)}">[图: 点击查看]</span>')
        i += 1; continue

    # Caption
    if is_caption(line):
        caption = re.sub(r'<a\s+id="[^"]*"></a>', '', line).strip()
        result.append(f'<p class="img-caption">{caption}</p>')
        i += 1; continue

    # Headings
    if line.startswith('# '):
        text = re.sub(r'<a\s+id="[^"]*"></a>', '', line[2:]).strip()
        result.append(f'<h2>{apply_entities(text)}</h2>')
        i += 1; continue
    if line.startswith('## '):
        text = re.sub(r'<a\s+id="[^"]*"></a>', '', line[3:]).strip()
        result.append(f'<h3>{apply_entities(text)}</h3>')
        i += 1; continue
    if line.startswith('### '):
        text = re.sub(r'<a\s+id="[^"]*"></a>', '', line[4:]).strip()
        result.append(f'<h4>{apply_entities(text)}</h4>')
        i += 1; continue

    # Regular paragraph
    text = line
    text = text.replace('\\.', '.').replace('\\-', '-').replace('\\[', '[').replace('\\(', '(').replace('\\"', '"')
    text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'<a\s+id="[^"]*"></a>', '', text)
    result.append(f'<p>{apply_entities(text)}</p>')
    i += 1

if toc_items:
    result.insert(result.index('<p>目 录</p>') + 1, '<p>\n' + '\n'.join(toc_items) + '\n</p>')

body_html = '\n'.join(result)

# Step 4: Replace chapter-body content
body_start = template.find('<div class="chapter-body')
body_end = template.find('</div>\n\n    <footer', body_start)

pre_body = template[:body_start]
post_body = template[body_end + len('</div>'):]

entity_legend = '<div class="chapter-body entity-annotated">\n                <div class="entity-legend"><span class="ent ent-星" title="恒星">恒星</span><span class="ent ent-官" title="星官">星官</span><span class="ent ent-曜" title="行星">行星</span><span class="ent ent-象" title="天象">天象</span><span class="ent ent-神" title="神祇">神祇</span><span class="ent ent-州" title="州县">州县</span><span class="ent ent-岁" title="纪年">纪年</span><span class="ent ent-器" title="仪器">仪器</span><span class="ent ent-历" title="历法">历法</span></div>\n<div class="entity-stats">共 <strong>0</strong> 处实体标注</div>\n'

new_html = pre_body + entity_legend + body_html + '\n            </div>' + post_body

# Step 5: Update header info and sidebar
new_html = new_html.replace('史记 · 天官书', '星庐·中国古天文学概论')
new_html = new_html.replace('西汉', '当代')
new_html = new_html.replace('作者：司马迁', '作者：桐安大司空（星庐）')
new_html = new_html.replace('成书：约前91年', '成书：2025年')
new_html = new_html.replace('卷数：1卷', '卷数：7章')
new_html = new_html.replace('中国现存最早的系统性天文学著作。将全天星官分为五宫（中东南西北），记录约90多个星官、500余颗恒星，叙述五星运行规律。',
    '作者有幸得先贤之伏藏，以太乙观星法为核心思想，系统性的复原了先秦时期我国真正的古天文学体系，为当代古天文领域的研究提供了全新的路径。')

# Sidebar active
new_html = new_html.replace('<li class="active"><a href="01_史记_天官书第五.html">', '<li><a href="01_史记_天官书第五.html">')
new_html = new_html.replace('<li><a href="20_星庐中国古天文学概论.html">', '<li class="active"><a href="20_星庐中国古天文学概论.html">')

# Entity count
ent_count = new_html.count('class="ent ent-')
new_html = re.sub(r'共 <strong>0</strong> 处实体标注', f'共 <strong>{ent_count}</strong> 处实体标注', new_html)

# Fix popup label JS: use caption text instead of "[图: 点击查看]"
old_js = "var l=document.createElement('div');l.className='img-label';l.textContent=ref.textContent;"
new_js = "var l=document.createElement('div');l.className='img-label';var cap=ref.nextElementSibling;while(cap&&!cap.classList.contains('img-caption'))cap=cap.nextElementSibling;l.textContent=cap?cap.textContent:'';"
new_html = new_html.replace(old_js, new_js)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Written: {OUTPUT_PATH}")
print(f"Size: {len(new_html):,} chars, {len(new_html.encode('utf-8')):,} bytes")
print(f"Entity spans: {ent_count}")
print(f"img-ref: {new_html.count('img-ref')}")
toc_count = new_html.count('href="#_Toc')
print(f"TOC links: {toc_count}")
