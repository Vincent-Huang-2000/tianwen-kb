import re
with open('docs/kg/timeline.html','r',encoding='utf-8') as f:
    h=f.read()
s=h.index('<script>')+8
e=h.index('</script>')
js=h[s:e]
m=re.search(r'var D=(\[\[.*?\]\]);',js,re.DOTALL)
if m:
    data_str=m.group(1)
    print(f'Data length: {len(data_str)}')
    quotes_total=sum(1 for ch in data_str if ch=='\u0022')
    print(f'Total double-quotes: {quotes_total} ({quotes_total%2})')
    # Check for potential JS-breaking characters
    for ch in '\u0000\u000a\u000d\u2028\u2029':
        if ch in data_str:
            print(f'FOUND problematic char: U+{ord(ch):04X}')
    print('Check complete')
else:
    print('Could not extract data')
