#!/usr/bin/env python3
"""Build Phase 3: Knowledge Graph data and visualizations."""
import json, re, os
from collections import defaultdict

# ============================================================
# 1. STAR OFFICIAL HIERARCHY (星官谱系树)
# ============================================================

star_tree = {
    "name": "中国星官体系",
    "children": [
        {
            "name": "三垣",
            "children": [
                {
                    "name": "紫微垣",
                    "description": "中宫，天帝居所",
                    "children": [
                        {"name": "北极五星", "children": [
                            {"name": "太子"}, {"name": "帝"}, {"name": "庶子"},
                            {"name": "后宫"}, {"name": "天枢"}
                        ]},
                        {"name": "四辅", "description": "辅弼之星"},
                        {"name": "勾陈", "children": [
                            {"name": "勾陈一（北极星）", "description": "帝星"}
                        ]},
                        {"name": "华盖", "children": [{"name": "杠"}]},
                        {"name": "六甲"}, {"name": "御女"}, {"name": "柱下史"},
                        {"name": "女史"}, {"name": "尚书"}, {"name": "大理"},
                        {"name": "阴德"}, {"name": "天床"},
                        {"name": "北斗七星", "children": [
                            {"name": "天枢（贪狼）"}, {"name": "天璇（巨门）"},
                            {"name": "天玑（禄存）"}, {"name": "天权（文曲）"},
                            {"name": "玉衡（廉贞）"}, {"name": "开阳（武曲）"},
                            {"name": "摇光（破军）"}
                        ]},
                        {"name": "文昌宫", "children": [
                            {"name": "上将"}, {"name": "次将"}, {"name": "贵相"},
                            {"name": "司命"}, {"name": "司中"}, {"name": "司禄"}
                        ]},
                        {"name": "三师"}, {"name": "太尊"}, {"name": "天牢"},
                        {"name": "太阳守"}, {"name": "势"}, {"name": "相"},
                        {"name": "玄戈"}, {"name": "天理"}, {"name": "内厨"},
                        {"name": "内阶"}, {"name": "八谷"}, {"name": "传舍"},
                        {"name": "阁道"}, {"name": "策星"},
                    ]
                },
                {
                    "name": "太微垣",
                    "description": "南宫，天庭政府",
                    "children": [
                        {"name": "五帝座", "description": "五方天帝"},
                        {"name": "内屏"}, {"name": "幸臣"}, {"name": "太子"},
                        {"name": "从官"}, {"name": "郎将"}, {"name": "虎贲"},
                        {"name": "常陈"}, {"name": "郎位"}, {"name": "明堂"},
                        {"name": "灵台"}, {"name": "少微"}, {"name": "长垣"},
                        {"name": "三台（三能）", "children": [
                            {"name": "上台"}, {"name": "中台"}, {"name": "下台"}
                        ]},
                    ]
                },
                {
                    "name": "天市垣",
                    "description": "天庭集市",
                    "children": [
                        {"name": "帝座"}, {"name": "候"}, {"name": "宦者"},
                        {"name": "斗"}, {"name": "斛"}, {"name": "列肆"},
                        {"name": "屠肆"}, {"name": "车肆"}, {"name": "宗正"},
                        {"name": "宗人"}, {"name": "宗"}, {"name": "帛度"},
                        {"name": "市楼"}, {"name": "天市左垣（十一国）"},
                        {"name": "天市右垣（十一国）"},
                    ]
                },
            ]
        },
        {
            "name": "二十八宿",
            "description": "沿黄道分布的二十八组星官",
            "children": [
                {
                    "name": "东方苍龙七宿",
                    "color": "#4a9b8e",
                    "children": [
                        {"name": "角宿", "description": "龙角", "stars": "角宿一（室女座α）"},
                        {"name": "亢宿", "description": "龙颈"},
                        {"name": "氐宿", "description": "龙胸"},
                        {"name": "房宿", "description": "龙腹"},
                        {"name": "心宿", "description": "龙心", "stars": "心宿二（天蝎座α，大火）"},
                        {"name": "尾宿", "description": "龙尾"},
                        {"name": "箕宿", "description": "龙粪"},
                    ]
                },
                {
                    "name": "南方朱雀七宿",
                    "color": "#c46b5a",
                    "children": [
                        {"name": "井宿", "description": "雀首"},
                        {"name": "鬼宿", "description": "雀目", "stars": "积尸气（M44蜂巢星团）"},
                        {"name": "柳宿", "description": "雀嘴"},
                        {"name": "星宿", "description": "雀颈", "stars": "星宿一（长蛇座α）"},
                        {"name": "张宿", "description": "雀嗉"},
                        {"name": "翼宿", "description": "雀翼"},
                        {"name": "轸宿", "description": "雀尾"},
                    ]
                },
                {
                    "name": "西方白虎七宿",
                    "color": "#c4a35a",
                    "children": [
                        {"name": "奎宿", "description": "虎尾"},
                        {"name": "娄宿", "description": "虎身"},
                        {"name": "胃宿", "description": "虎胃"},
                        {"name": "昴宿", "description": "虎头", "stars": "昴星团（M45七姊妹星团）"},
                        {"name": "毕宿", "description": "虎口"},
                        {"name": "觜宿", "description": "虎须"},
                        {"name": "参宿", "description": "虎前肢", "stars": "参宿四（猎户座α）、参宿七"},
                    ]
                },
                {
                    "name": "北方玄武七宿",
                    "color": "#6b8db5",
                    "children": [
                        {"name": "斗宿", "description": "龟首蛇身"},
                        {"name": "牛宿", "description": "牵牛"},
                        {"name": "女宿", "description": "婺女"},
                        {"name": "虚宿", "description": "虚耗"},
                        {"name": "危宿", "description": "危屋"},
                        {"name": "室宿", "description": "营室"},
                        {"name": "壁宿", "description": "东壁"},
                    ]
                },
            ]
        },
        {
            "name": "近南极星区",
            "children": [
                {"name": "海山"}, {"name": "十字架"}, {"name": "马尾"},
                {"name": "马腹"}, {"name": "蜜蜂"}, {"name": "三角形"},
                {"name": "异雀"}, {"name": "孔雀"}, {"name": "波斯"},
                {"name": "蛇尾"}, {"name": "蛇腹"}, {"name": "蛇首"},
                {"name": "鸟喙"}, {"name": "鹤"}, {"name": "火鸟"},
                {"name": "水委"}, {"name": "附白"}, {"name": "夹白"},
                {"name": "金鱼"}, {"name": "海石"}, {"name": "飞鱼"},
                {"name": "南船"}, {"name": "小斗"},
            ]
        },
    ]
}

os.makedirs('data', exist_ok=True)
with open('data/star_tree.json', 'w', encoding='utf-8') as f:
    json.dump(star_tree, f, ensure_ascii=False, indent=2)
print(f"Star tree: {len(star_tree['children'])} root branches")

# ============================================================
# 2. CROSS-BOOK EVENT MATCHING
# ============================================================

with open('data/events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

# Group events by (year, type) to find cross-book matches
by_year_type = defaultdict(list)
for ev in events:
    key = (ev['year'], ev['type'])
    by_year_type[key].append(ev)

# Find events with multiple sources
cross_book = []
for key, ev_list in by_year_type.items():
    sources = set(ev['source'] for ev in ev_list)
    if len(sources) >= 2:
        cross_book.append({
            'year': key[0],
            'type': key[1],
            'count': len(ev_list),
            'sources': sorted(sources),
            'events': ev_list,
        })

cross_book.sort(key=lambda x: x['year'])

print(f"Cross-book events: {len(cross_book)}")
for cb in cross_book[:5]:
    print(f"  {cb['year']:>5} {cb['type']:15s} {len(cb['sources'])} sources: {', '.join(cb['sources'][:3])}")

with open('data/cross_book_events.json', 'w', encoding='utf-8') as f:
    json.dump(cross_book, f, ensure_ascii=False, indent=2)

# ============================================================
# 3. ASTROLOGICAL CORRESPONDENCES
# ============================================================

# Scan corpus for "X → Y" type patterns
correspondences = []

# Known astrological patterns
patterns = [
    (r'日[有]?食[之]?.*?(?:主|为|则|应|占[曰]?)(.{4,40}?)(?:[。；]|$)', '日食'),
    (r'月[有]?食[之]?.*?(?:主|为|则|应)(.{4,40}?)(?:[。；]|$)', '月食'),
    (r'彗[星孛].*?(?:主|为|则|应|占).{0,20}(.{4,50}?)(?:[。；]|$)', '彗星'),
    (r'[荧太岁填辰]..(?:犯|守|入|掩)(.{2,8}).*?(?:主|为|则|应|兵|丧|旱|水|饥|疫|君|臣)(.{4,40}?)(?:[。；]|$)', '星犯'),
    (r'(?:流星|星陨|陨星).*?(?:主|为|则|应)(.{4,40}?)(?:[。；]|$)', '流星'),
    (r'客星.*?(?:主|为|则|应)(.{4,40}?)(?:[。；]|$)', '客星'),
]

# Check corpus files
for fn in sorted(os.listdir('corpus')):
    if not fn.endswith('.txt') or '_tagged' in fn: continue
    with open(os.path.join('corpus', fn), 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Clean entity brackets
    clean = re.sub(r'\[[^\]]+\]', '', text)
    
    for pat, etype in patterns:
        for m in re.finditer(pat, clean):
            consequence = m.group(1).strip() if m.lastindex else m.group(0).strip()
            if len(consequence) < 4: continue
            correspondences.append({
                'type': etype,
                'consequence': consequence[:80],
                'source': fn.split('_')[0] if '_' in fn else fn,
                'match': m.group(0)[:120],
            })

# Dedup and sort
seen = set()
unique_corr = []
for c in correspondences:
    key = (c['type'], c['consequence'][:30])
    if key not in seen:
        seen.add(key)
        unique_corr.append(c)

unique_corr.sort(key=lambda x: x['type'])

print(f"\nAstrological correspondences: {len(unique_corr)}")
by_type = defaultdict(int)
for c in unique_corr:
    by_type[c['type']] += 1
for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
    print(f"  {t}: {n}")

with open('data/astrology.json', 'w', encoding='utf-8') as f:
    json.dump(unique_corr, f, ensure_ascii=False, indent=2)

print("\nAll data files created.")
