import re

with open(r'D:\24history\twz\星庐中国古天文学概论.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Test all TOC entries
pat = re.compile(r'\[(.+?)(?:\t\d+)?\]\((#_[^)]+)\)')

toc_start = None
for i, line in enumerate(lines):
    if '目 录' in line:
        toc_start = i
        break

failures = 0
for i in range(toc_start + 1, len(lines)):
    line = lines[i]
    if not line.strip():
        continue
    if line.startswith('#') or (line.startswith('<a') and not line.strip().startswith('<a id')):
        break
    
    if line.startswith('['):
        m = pat.match(line)
        if not m:
            failures += 1
            if failures <= 5:
                print(f'FAIL line {i+1}: {repr(line[:100])}')

print(f'Total failures: {failures}')
