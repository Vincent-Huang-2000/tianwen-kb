import re, os
from html import unescape

ENTITIES = []

for name in [
    # 星官
    "紫宫", "紫微垣", "太微垣", "天市垣", "北斗七星", "文昌宫",
    "三能", "三台", "天枪", "天棓", "阁道", "阴德",
    "营室", "东壁", "天驷", "天市", "市楼", "骑官", "少微", "轩辕",
    "东井", "舆鬼", "天库楼", "天苑", "九游", "天厕", "天矢",
    "羽林天军", "离宫", "天潢", "河鼓", "建星", "天关", "天门",
    "咸池", "天五潢", "摄提", "南门", "天阙", "天街", "天牢",
    "南河", "北河", "北落", "司空", "天狼",
    "天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光",
    "勾陈", "华盖", "五车", "弧矢", "天纲", "天津", "天船",
    "天廪", "天樽", "天庙", "天稷", "天钱", "天桴", "天垒城",
    "大陵", "螣蛇", "北落师门", "十二国",
    "北极五星", "四辅", "六甲", "女御", "柱下史", "女史", "尚书",
    "大理", "天床", "三师", "太尊", "太阳守", "玄戈", "天理",
    "内厨", "内阶", "八谷", "传舍", "策星", "造父",
    "附路", "积水", "积薪", "天谗", "参旗", "天园", "九斿",
    "军市", "野鸡", "天社", "天纪", "水位", "四渎", "阙丘",
    "爟星", "酒旗", "东瓯", "器府", "军门", "土司空",
    "青丘", "败臼", "离瑜", "扶筐", "奚仲", "車府",
    "败瓜", "雷电", "云雨", "霹雳", "鈇锧", "八魁",
    "灵台", "明堂",
]:
    ENTITIES.append(("官", name))

for name in [
    "天极星", "辅星", "招摇", "天锋", "织女", "王良", "附耳",
    "南极老人", "蚩尤之旗", "天狗", "格泽", "旬始", "枉矢",
    "天欃", "天椐", "北落", "长沙", "北极星",
    "五帝座", "太子星", "庶子星", "后宫星", "天乙", "太乙",
]:
    ENTITIES.append(("星", name))

for name in ["岁星", "荧惑", "填星", "镇星", "太白", "辰星"]:
    ENTITIES.append(("曜", name))

for name in [
    "日食", "月食", "彗星", "流星", "客星", "新星",
    "日晕", "月晕", "孛星", "长星", "蓬星", "含誉", "景星", "归邪",
]:
    ENTITIES.append(("象", name))

for name in ["太一", "天一", "五帝", "黄帝", "皇天", "上帝", "后土"]:
    ENTITIES.append(("神", name))

for name in [
    "雍州", "冀州", "兖州", "青州", "徐州", "扬州", "荆州", "豫州", "梁州",
    "幽州", "并州", "益州", "交州", "朔方", "凉州",
    "三河", "河内", "河南", "河东", "巴蜀", "陇西", "河西",
    "江淮", "江南", "岭南", "匈奴", "大宛", "朝鲜",
]:
    ENTITIES.append(("州", name))

for name in [
    "摄提格", "单阏", "执徐", "大荒骆", "敦牂", "叶洽",
    "涒滩", "作鄂", "阉茂", "大渊献", "困敦", "赤奋若",
]:
    ENTITIES.append(("岁", name))

for name in [
    "浑天仪", "简仪", "仰仪", "圭表", "漏刻", "水运仪象台", "候风地动仪", "晷影",
]:
    ENTITIES.append(("器", name))

for name in [
    "太初历", "三统历", "四分历", "乾象历", "景初历", "元嘉历",
    "大明历", "皇极历", "麟德历", "大衍历", "宣明历", "应天历",
    "乾元历", "仪天历", "崇天历", "明天历", "奉元历", "观天历",
    "纪元历", "统元历", "乾道历", "淳熙历", "会元历", "统天历",
    "开禧历", "成天历", "授时历", "大统历",
    "甘石星经", "灵宪", "浑天仪注", "开元占经",
]:
    ENTITIES.append(("历", name))

ENTITIES.sort(key=lambda x: len(x[1]), reverse=True)

COLORS = {
    '星': '#FFD700', '官': '#7DC2B2', '曜': '#F49B8A',
    '象': '#FF6B6B', '神': '#C9A96E', '州': '#7EB8DA',
    '岁': '#6B8DB5', '器': '#D4A574', '历': '#B39DDB',
}
TYPES_CN = {
    '星': '恒星', '官': '星官', '曜': '行星',
    '象': '天象', '神': '神祇', '州': '州县',
    '岁': '纪年', '器': '仪器', '历': '历法',
}

css_rules = ['.ent{cursor:help;font-weight:500;border-bottom:1px dotted;padding:0 1px;transition:filter 0.2s,text-shadow 0.2s}',
             '.ent:hover{filter:brightness(1.3);text-shadow:0 0 8px currentColor}']
for t, c in COLORS.items():
    css_rules.append('.ent-{}{{color:{};border-color:{}88}}'.format(t, c, c))

ENTITY_CSS = '    <style>\n/* Entity syntax highlighting */\n' + ' '.join(css_rules) + '''
.entity-legend {
    display: flex; flex-wrap: wrap; gap: 10px 20px; margin-bottom: 12px;
    padding: 10px 16px; background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 8px;
}
.entity-legend .ent { font-size: 0.85rem; }
.entity-stats {
    font-size: 0.8rem; color: var(--text-muted); margin-bottom: 24px;
    padding-bottom: 12px; border-bottom: 1px solid var(--border);
}
</style>'''

LEGEND = ''.join('<span class="ent ent-{}" title="{}">{}</span>'.format(t, TYPES_CN[t], TYPES_CN[t])
                 for t in ['星','官','曜','象','神','州','岁','器','历'])

chapters_dir = 'docs/chapters'
files = sorted([f for f in os.listdir(chapters_dir)
                if f.endswith('.html') and f != '01_史记_天官书第五.html'])

grand_total = 0
grand_chars = 0
processed = 0

for fn in files:
    fpath = os.path.join(chapters_dir, fn)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    body_match = re.search(r'<div class="chapter-body">(.*?)</main>', html, re.DOTALL)
    if not body_match:
        print('SKIP {}: no body'.format(fn))
        continue

    body_html = body_match.group(1)
    clean = re.sub(r'<br\s*/?>', '\n', body_html)
    clean = re.sub(r'<[^>]+>', '', clean)
    clean = unescape(clean)
    clean = re.sub(r'\n{3,}', '\n\n', clean).strip()

    annotated = clean
    for typ, surface in ENTITIES:
        annotated = re.sub(re.escape(surface), '[' + typ + ' ' + surface + ']', annotated)

    for _ in range(10):
        old = annotated
        annotated = re.sub(r'\[(\S+) \[(\S+) ([^\]]+?)\] ([^\]]+?)\]', r'[\1 \3\4]', annotated)
        annotated = re.sub(r'\[岁 \[官 ([^\]]+)\]\] ([^\]]+?)\]', r'[岁 \1\2]', annotated)
        if annotated == old:
            break

    annotated = re.sub(r'\n{3,}', '\n\n', annotated)

    tag_name = fn.replace('.html', '.txt')
    os.makedirs('corpus', exist_ok=True)
    with open(os.path.join('corpus', tag_name), 'w', encoding='utf-8') as f:
        f.write(annotated)

    counts = {}
    for t in COLORS:
        counts[t] = len(re.findall(r'\[' + t + r' ', annotated))
    total = sum(counts.values())
    grand_total += total
    grand_chars += len(clean)

    lines = annotated.split('\n')
    body_parts = []
    in_p = False
    for line in lines:
        s = line.strip()
        if not s:
            if in_p:
                body_parts.append('</p>')
                in_p = False
            continue
        if not in_p:
            body_parts.append('<p>')
            in_p = True
        s = re.sub(
            r'\[(\S+) ([^\]]+?)\]',
            lambda m: '<span class="ent ent-{}" title="{}：{}">{}</span>'.format(
                m.group(1), TYPES_CN.get(m.group(1), m.group(1)), m.group(2), m.group(2)),
            s
        )
        body_parts.append(s)
    if in_p:
        body_parts.append('</p>')
    body_html_out = '\n'.join(body_parts)

    stat_parts = ['{} {}'.format(TYPES_CN[t], counts[t]) for t in ['星','官','曜','象','神','州','岁','器','历'] if counts[t] > 0]

    new_body = '            <div class="chapter-body entity-annotated">\n                <div class="entity-legend">{}</div>\n                <div class="entity-stats">共 <strong>{}</strong> 处实体标注：{}</div>\n{}\n            </div>'.format(
        LEGEND, total, ' · '.join(stat_parts), body_html_out)

    if '/* Entity syntax highlighting */' not in html:
        html = html.replace('</head>', ENTITY_CSS + '\n</head>')

    body_div_start = html.find('<div class="chapter-body')
    main_end = html.find('</main>', body_div_start)
    if body_div_start >= 0 and main_end >= 0:
        old_body = html[body_div_start:main_end]
        html = html.replace(old_body, new_body + '\n')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    processed += 1
    if processed % 3 == 0:
        print('{}/19 done...'.format(processed))

print('\n' + '='*60)
print('Processed: {} files'.format(processed))
print('Total chars: {:,}'.format(grand_chars))
print('Total entities: {:,}'.format(grand_total))
print('Avg density: {:.1f}%'.format(grand_total/max(grand_chars,1)*100))
