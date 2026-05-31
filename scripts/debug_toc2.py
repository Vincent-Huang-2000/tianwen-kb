import re

with open(r'D:\24history\twz\星庐中国古天文学概论.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find TOC start
toc_start = None
for i, line in enumerate(lines):
    if '目 录' in line:
        toc_start = i
        break

# Simulate the converter loop from toc_start
in_toc = False
toc_items = []
i = toc_start + 1  # Start after 目 录

while i < len(lines):
    line = lines[i].rstrip('\n')
    if not line.strip():
        i += 1; continue
    
    if in_toc:
        m = re.match(r'\[(.+?)(?:\t\d+)?\]\((#_[^)]+)\)', line)
        if m:
            toc_text = m.group(1).replace('\\.', '.')
            toc_items.append(f'<a href="{m.group(2)}">{toc_text}</a>')
            if len(toc_items) == 1:
                print(f'First TOC match: {repr(toc_text[:30])}')
            i += 1; continue
        elif line.startswith('#'):
            print(f'Heading found at i={i}: {line[:50]}')
            in_toc = False
            break
        else:
            if i <= toc_start + 5:
                print(f'TOC line NOT matched at i={i}: {repr(line[:60])}')
            i += 1; continue

print(f'TOC items collected: {len(toc_items)}')

# Now reset and test with in_toc correctly set
in_toc = True
toc_items = []
i = toc_start + 1
print('\n--- With in_toc=True ---')
while i < len(lines):
    line = lines[i].rstrip('\n')
    if not line.strip():
        i += 1; continue
    
    m = re.match(r'\[(.+?)(?:\t\d+)?\]\((#_[^)]+)\)', line)
    if m:
        toc_items.append(m.group(1))
        if len(toc_items) <= 3:
            print(f'Match: {repr(m.group(1)[:30])}')
        i += 1; continue
    elif line.startswith('#'):
        print(f'End at i={i}: {line[:50]}')
        break
    else:
        print(f'No match at i={i}: {repr(line[:60])}')
        break

print(f'Items: {len(toc_items)}')
