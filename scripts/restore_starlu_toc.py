import re
from urllib.parse import quote

corpus_path = r"D:\24history\twz\tianwen-kb\corpus\20_星庐中国古天文学概论.txt"
html_path = r"D:\24history\twz\tianwen-kb\docs\chapters\20_星庐中国古天文学概论.html"

with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_lines = f.readlines()

# Find TOC: from line with "目 录" to the line before "摘要：中国古天文学..."
toc_start = None
toc_end = None
for i, line in enumerate(corpus_lines):
    s = line.strip()
    if s == '目 录':
        toc_start = i + 1  # skip "目 录" line itself
    if toc_start and i > toc_start and s.startswith('摘要：') and '中国古天文' in s:
        toc_end = i
        break

toc_lines = [l.rstrip('\n') for l in corpus_lines[toc_start:toc_end]]
print(f"TOC: lines {toc_start+1}-{toc_end} ({len(toc_lines)} lines)")
for l in toc_lines[:5]:
    print(f"  {l[:80]}")

TYPE_MAP = {
    '星': '恒星', '官': '星官', '曜': '行星', '象': '天象',
    '神': '神祇', '州': '州县', '岁': '纪年', '器': '仪器', '历': '历法'
}
REF_FILE = '20_星庐中国古天文学概论.html'

def convert_annotation(text):
    def repl(m):
        t = m.group(1)
        name = m.group(2)
        type_cn = TYPE_MAP.get(t, t)
        url_name = quote(name, safe='')
        return f'<span class="ent ent-{t}" title="{type_cn}：{name}" style="cursor:pointer" onclick="window.open(\'../kg/entity.html?name={url_name}&ref={REF_FILE}\',\'_blank\')">{name}</span>'
    return re.sub(r'\[(\S+) ([^\]]+)\]', repl, text)

# Build TOC HTML exactly matching original format
toc_html = '<p>\n目 录\n</p>\n<p>\n'
for i, line in enumerate(toc_lines):
    converted = convert_annotation(line)
    toc_html += converted + '\n'
toc_html += '</p>'

print(f"\nTOC HTML: {len(toc_html)} chars")

# Replace in HTML file
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find the toc-nav div and the duplicate p block
# Pattern: <div class="toc-nav">...toc...</div>\n<p>\n摘要：\n...old TOC...\n</p>\n<p>\n摘要：...
# Target: replace from toc-nav start to before the real content's <p>\n摘要：\n中国...

toc_nav_start = html_content.find('<div class="toc-nav">')
# After toc-nav div + old TOC p, find the real "摘要：中国" content
real_content_marker = html_content.find('<p>\n摘要：\n中国古天文', toc_nav_start)

if toc_nav_start == -1:
    print("ERROR: toc-nav not found!")
elif real_content_marker == -1:
    print("ERROR: real content marker not found!")
else:
    old_block = html_content[toc_nav_start:real_content_marker]
    new_html = html_content[:toc_nav_start] + toc_html + '\n' + html_content[real_content_marker:]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Replaced {len(old_block)} chars with {len(toc_html)} chars")
    
    # Verify
    count_toc = new_html.count('目 录')
    has_tocnav = 'class="toc-nav"' in new_html
    print(f"'目 录' count: {count_toc} (should be 1)")
    print(f"toc-nav CSS: {has_tocnav} (OK in <style>)")
    # Check for entity spans in TOC
    ent_count = new_html.count('class="ent ent-')
    print(f"Entity spans total: {ent_count}")
