#!/usr/bin/env python3
"""Comprehensive omen enrichment for all events."""
import json, re, os
from collections import defaultdict

BOOK_NAMES = {
    'book_01': '史记·天官书', 'book_02': '汉书·天文志', 'book_03': '后汉书·天文志',
    'book_04': '晋书·天文志', 'book_05': '宋书·天文志', 'book_06': '南齐书·天文志',
    'book_07': '魏书·天象志', 'book_08': '隋书·天文志', 'book_09': '旧唐书·天文志',
    'book_10': '新唐书·天文志', 'book_11': '旧五代史·天文志', 'book_12': '新五代史·司天考',
    'book_13': '宋史·天文志', 'book_14': '辽史·历象志', 'book_15': '金史·天文志',
    'book_16': '元史·天文志', 'book_17': '明史·天文志',
}
NAME_TO_KEY = {v: k for k, v in BOOK_NAMES.items()}

corpus = {}
for fn in sorted(os.listdir('corpus')):
    if not fn.endswith('.txt') or '_tagged' in fn: continue
    prefix = fn.split('_')[0]
    key = 'book_' + prefix
    with open(os.path.join('corpus', fn), 'r', encoding='utf-8') as f:
        corpus[key] = f.read()

with open('data/events.json', 'r', encoding='utf-8') as f:
    events = json.load(f)

OMEN_PATTERNS = [
    r'占曰[：:\s]*([^。；]{4,80}?)(?:[。；]|$)',
    r'占[：:]\s*([^。；]{4,80}?)(?:[。；]|$)',
    r'主([^。；]{4,60}?)(?:[。；]|$)',
    r'[所为]应([^。；]{4,60}?)(?:[。；]|$)',
    r'其[国分野][，,]?([^。；]{4,50}?)(?:[。；]|$)',
]

def extract_omen(text, event_desc):
    clean = re.sub(r'\[[^\]]+\]', '', text)
    short = event_desc[:40]
    idx = clean.find(short)
    if idx < 0: return ''
    ctx = clean[max(0,idx-50):idx+len(event_desc)+250]
    omens = []
    for pat in OMEN_PATTERNS:
        for m in re.finditer(pat, ctx):
            omen = m.group(1).strip() if m.lastindex else m.group(0).strip()
            if len(omen) < 6: continue
            if re.search(r'^[日月星辰宿度分舍]', omen): continue
            omens.append(omen)
    for o in omens:
        if any(kw in o for kw in ['兵','丧','亡','旱','水','饥','疫','君','臣','王','乱','诛','杀','战','忧']):
            return o[:100]
    return omens[0][:100] if omens else ''

enriched = 0
for ev in events:
    src = ev.get('source', '')
    key = NAME_TO_KEY.get(src)
    if key and key in corpus:
        omen = extract_omen(corpus[key], ev['description'])
        if omen:
            ev['omen'] = omen
            enriched += 1

print('Enriched: {}/{}'.format(enriched, len(events)))

ot = defaultdict(int)
tt = defaultdict(int)
for ev in events:
    tt[ev['type']] += 1
    if ev.get('omen'): ot[ev['type']] += 1
for t in sorted(tt):
    print('  {}: {}/{}'.format(t, ot[t], tt[t]))

with open('data/events.json', 'w', encoding='utf-8') as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

# Rebuild cross_book
bk = defaultdict(list)
for ev in events:
    bk[(ev['year'],ev['type'])].append(ev)
cb = []
for key, evs in bk.items():
    srcs = set(ev['source'] for ev in evs)
    if len(srcs) >= 2:
        cb.append({'year':key[0],'type':key[1],'count':len(evs),'sources':sorted(srcs),'events':evs})
cb.sort(key=lambda x:x['year'])
with open('data/cross_book_events.json','w',encoding='utf-8') as f:
    json.dump(cb,f,ensure_ascii=False,indent=2)

print('Cross-book: {}'.format(len(cb)))
print('Rebuilt data files')
