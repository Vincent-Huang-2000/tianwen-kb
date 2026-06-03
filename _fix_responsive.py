"""Apply responsive layout fixes to style.css and index.html"""
import os

base = r'D:\24history\twz\tianwen-kb\docs'

# ============================================================
# CSS
# ============================================================
css_path = os.path.join(base, 'css', 'style.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

replacements = [
    # 1. html overflow-x
    ('    -moz-osx-font-smoothing: grayscale;\n}',
     '    -moz-osx-font-smoothing: grayscale;\n    overflow-x: hidden;\n}'),
    # 2. body overflow-x (first occurrence in body block)
    ('    user-select: none;\n}\n\n/* --- Links --- */',
     '    user-select: none;\n    overflow-x: hidden;\n}\n\n/* --- Links --- */'),
    # 3. nav-inner gap + min-width
    ('    justify-content: space-between;\n}\n\n.nav-logo {',
     '    justify-content: space-between;\n    gap: 16px;\n    min-width: 0;\n}\n\n.nav-logo {'),
    # 4. nav-logo ellipsis
    ('    white-space: nowrap;\n}\n\n.nav-logo:hover {',
     '    white-space: nowrap;\n    overflow: hidden;\n    text-overflow: ellipsis;\n}\n\n.nav-logo:hover {'),
    # 5. nav-links flex-shrink + white-space
    ('    gap: 6px;\n}\n\n.nav-links a {',
     '    gap: 6px;\n    flex-shrink: 0;\n    white-space: nowrap;\n}\n\n.nav-links a {'),
    # 6. nav-links a flex
    ('    border-radius: var(--radius-sm);\n    transition: color 0.2s ease, background 0.2s ease;\n}\n\n.nav-links a:hover {',
     '    border-radius: var(--radius-sm);\n    transition: color 0.2s ease, background 0.2s ease;\n    flex: 0 0 auto;\n    white-space: nowrap;\n}\n\n.nav-links a:hover {'),
    # 7. chapters-grid width + grid-template-columns
    ('.chapters-grid {\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 48px 24px 64px;\n    display: grid;\n    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));\n    gap: 20px;\n}',
     '.chapters-grid {\n    width: 100%;\n    max-width: 1200px;\n    margin: 0 auto;\n    padding: 48px 24px 64px;\n    display: grid;\n    grid-template-columns: repeat(auto-fill, minmax(min(300px, 100%), 1fr));\n    gap: 20px;\n}'),
    # 8. chapter-card min-width
    ('.chapter-card {\n    background: var(--bg-card);\n    border: 1px solid var(--border);\n    border-radius: var(--radius-lg);\n    padding: 24px;\n    transition:',
     '.chapter-card {\n    min-width: 0;\n    background: var(--bg-card);\n    border: 1px solid var(--border);\n    border-radius: var(--radius-lg);\n    padding: 24px;\n    transition:'),
    # 9. 980px breakpoint before 768px
    ('   RESPONSIVE BREAKPOINTS\n   ============================================================ */\n@media (max-width: 768px) {',
     '   RESPONSIVE BREAKPOINTS\n   ============================================================ */\n@media (max-width: 980px) {\n    /* 中等窄屏固定为两列，避免三列临界宽度时右侧卡片被裁切。 */\n    .chapters-grid {\n        grid-template-columns: repeat(2, minmax(0, 1fr));\n    }\n}\n\n@media (max-width: 768px) {'),
    # 10. 768px nav-logo flex
    ('    .nav-logo {\n        font-size: 1rem;\n    }\n\n    .nav-links {\n        gap: 0;\n    }',
     '    .nav-logo {\n        font-size: 1rem;\n        flex: 1 1 auto;\n    }\n\n    .nav-links {\n        gap: 0;\n        flex: 0 1 auto;\n        max-width: 58vw;\n        overflow-x: auto;\n        overflow-y: hidden;\n        -webkit-overflow-scrolling: touch;\n        scrollbar-width: none;\n    }\n\n    /* 窄屏导航保持单行横向滚动，避免菜单换行撑高顶部栏。 */\n    .nav-links::-webkit-scrollbar {\n        display: none;\n    }'),
    # 11. 768px nav-links a flex
    ('    .nav-links a {\n        font-size: 0.8rem;\n        padding: 6px 8px;\n    }\n\n    /* --- Chapter Layout:',
     '    .nav-links a {\n        font-size: 0.8rem;\n        padding: 6px 8px;\n        flex: 0 0 auto;\n    }\n\n    /* --- Chapter Layout:'),
    # 12. 480px nav-logo max-width + nav-links max-width
    ('@media (max-width: 480px) {\n    .nav-links a {\n        font-size: 0.72rem;\n        padding: 4px 6px;\n    }',
     '@media (max-width: 480px) {\n    .nav-logo {\n        max-width: 42vw;\n    }\n\n    .nav-links {\n        max-width: 54vw;\n    }\n\n    .nav-links a {\n        font-size: 0.72rem;\n        padding: 4px 6px;\n    }'),
]

for i, (old, new) in enumerate(replacements):
    if old not in css:
        print(f"CSS #{i+1}: MATCH NOT FOUND! Skipping.")
        print(f"  Looking for: {repr(old[:80])}...")
        continue
    css = css.replace(old, new)
    print(f"CSS #{i+1}: OK")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)
print(f"\nCSS written: {len(css)} bytes")

# ============================================================
# index.html
# ============================================================
idx_path = os.path.join(base, 'index.html')
with open(idx_path, 'r', encoding='utf-8') as f:
    idx = f.read()

idx_replacements = [
    # 1. hero-timeline width + overflow
    ('.hero-timeline {\n            max-width: 1200px;\n            margin: 0 auto;\n            padding: 20px 24px 0;\n            position: relative;\n        }',
     '.hero-timeline {\n            width: 100%;\n            max-width: 1200px;\n            margin: 0 auto;\n            padding: 20px 24px 0;\n            position: relative;\n            overflow: hidden;\n        }'),
    # 2. timeline-strip overflow-y + max-width
    ('            overflow-x: auto;\n            padding: 16px 0 24px;\n            gap: 4px;\n            scrollbar-width: thin;',
     '            overflow-x: auto;\n            overflow-y: hidden;\n            padding: 16px 0 24px;\n            gap: 4px;\n            max-width: 100%;\n            overscroll-behavior-x: contain;\n            scrollbar-width: thin;'),
    # 3. 768px hero-timeline padding
    ('@media (max-width: 768px) {\n            .hero-stats {\n                gap: 28px;\n            }\n\n            .stat-number {',
     '@media (max-width: 768px) {\n            .hero-stats {\n                gap: 28px;\n            }\n\n            .hero-timeline {\n                padding-left: 16px;\n                padding-right: 16px;\n            }\n\n            .stat-number {'),
    # 4. 480px timeline-strip flex-start
    ('@media (max-width: 480px) {\n            .hero-stats {\n                gap: 20px;\n            }\n\n            .stat-number {',
     '@media (max-width: 480px) {\n            .hero-stats {\n                gap: 20px;\n            }\n\n            /* 手机端保留时间轴内部滚动，不再撑开整个页面背景。 */\n            .timeline-strip {\n                justify-content: flex-start;\n            }\n\n            .stat-number {'),
    # 5. canvas max-width
    ('        #dunhuang-stars {\n            position: absolute;\n            top: 0;\n            left: 0;\n            width: 100%;\n            height: 100%;',
     '        #dunhuang-stars {\n            position: absolute;\n            top: 0;\n            left: 0;\n            width: 100%;\n            max-width: 100%;\n            height: 100%;'),
]

for i, (old, new) in enumerate(idx_replacements):
    if old not in idx:
        print(f"IDX #{i+1}: MATCH NOT FOUND! Skipping.")
        print(f"  Looking for: {repr(old[:80])}...")
        continue
    idx = idx.replace(old, new)
    print(f"IDX #{i+1}: OK")

with open(idx_path, 'w', encoding='utf-8') as f:
    f.write(idx)
print(f"\nindex.html written: {len(idx)} bytes")
print("\n=== DONE ===")
