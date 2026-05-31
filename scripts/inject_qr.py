import os

SCRIPT = '<script src="{}js/qr-popup.js"></script>\n'
found = 0
ok = 0
skipped = 0

DOCS = r"D:\24history\twz\tianwen-kb\docs"

for root, dirs, files in os.walk(DOCS):
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, DOCS).replace('\\', '/')
        depth = rel.count('/')
        if depth > 1:
            continue
        
        prefix = '' if depth == 0 else '../'
        
        with open(fp, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        found += 1
        
        if 'qr-popup.js' in content:
            print(f"  SKIP: {rel}")
            skipped += 1
            continue
        
        body_end = content.rfind('</body>')
        if body_end == -1:
            print(f"  SKIP (no </body>): {rel}")
            continue
        
        new_content = content[:body_end] + SCRIPT.format(prefix) + content[body_end:]
        with open(fp, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        ok += 1
        print(f"  OK: {rel}")

print(f"\nFound: {found}, OK: {ok}, Skipped: {skipped}")
