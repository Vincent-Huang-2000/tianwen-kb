# Event extraction from tagged astronomy texts
import re, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from dynasty_map import resolve_year, BOOK_DYNASTY, DYNASTY_MAP

# Event type patterns
EVENT_TYPES = {
    '日食': ['日食', '日有食', '日有蚀', '日蚀'],
    '月食': ['月食', '月有食', '月蚀'],
    '彗星': ['彗星', '彗', '星孛', '孛星', '长星', '蓬星'],
    '流星': ['流星', '星陨', '陨星', '星坠'],
    '客星': ['客星', '新星'],
    '日晕': ['日晕', '日珥', '日戴', '日冠'],
    '月晕': ['月晕', '月珥'],
    '行星': ['岁星', '荧惑', '太白', '辰星', '填星', '五星聚', '星合'],
}

# Source book mapping
BOOK_INFO = {
    '01': ('史记', '天官书', '司马迁', '西汉'),
    '02': ('汉书', '天文志', '班固', '东汉'),
    '03': ('后汉书', '天文志', '范晔', '刘宋'),
    '04': ('晋书', '天文志', '房玄龄、李淳风等', '唐'),
    '05': ('宋书', '天文志', '沈约', '梁'),
    '06': ('南齐书', '天文志', '萧子显', '梁'),
    '07': ('魏书', '天象志', '魏收', '北齐'),
    '08': ('隋书', '天文志', '魏徵、李淳风等', '唐'),
    '09': ('旧唐书', '天文志', '刘昫等', '后晋'),
    '10': ('新唐书', '天文志', '欧阳修等', '宋'),
    '11': ('旧五代史', '天文志', '薛居正等', '宋'),
    '12': ('新五代史', '司天考', '欧阳修', '宋'),
    '13': ('宋史', '天文志', '脱脱等', '元'),
    '14': ('辽史', '历象志', '脱脱等', '元'),
    '15': ('金史', '天文志', '脱脱等', '元'),
    '16': ('元史', '天文志', '宋濂等', '明'),
    '17': ('明史', '天文志', '张廷玉等', '清'),
    '18': ('步天歌', '', '王希明', '唐'),
    '19': ('乙巳占', '', '李淳风', '唐'),
    '20': ('星庐', '中国古天文学概论', '桐安大司空', '现代'),
}

def extract_events(text, book_prefix, source_book, source_chapter):
    """Extract dated astronomical events from text."""
    events = []
    
    # Split into sentences
    sentences = re.split(r'[。；\n]', text)
    
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 8:
            continue
        
        # Check for event keywords
        event_type = None
        for etype, keywords in EVENT_TYPES.items():
            for kw in keywords:
                if kw in sent:
                    event_type = etype
                    break
            if event_type:
                break
        
        if not event_type:
            continue
        
        # Try to extract date
        ce_year = extract_date(sent, book_prefix)
        if ce_year is None:
            ce_year = extract_date_simple(sent, book_prefix)
        
        # Filter out theoretical/general statements
        if is_theoretical(sent):
            continue
        
        # Create event record
        event = {
            'year': ce_year,
            'type': event_type,
            'description': sent.strip()[:200],
            'source_book': source_book,
            'source_chapter': source_chapter,
            'source_prefix': book_prefix,
        }
        events.append(event)
    
    return events

def extract_date(sent, book_prefix):
    """Extract date from sentence: look for 年号 patterns."""
    # Pattern: XXXX年 (reign year)
    # Common formats:
    # - 元兴元年
    # - 永平三年
    # - 贞观元年闰三月
    # - 文帝前元二年
    
    # Try full reign name + year
    # Get all possible reign names for this book's dynasty
    dynasty = BOOK_DYNASTY.get(book_prefix, '')
    if dynasty and dynasty in DYNASTY_MAP:
        reigns = list(DYNASTY_MAP[dynasty].keys())
        # Sort by length descending
        reigns.sort(key=len, reverse=True)
        for reign in reigns:
            pattern = reign + r'([一二三四五六七八九十百千\d]+)年'
            m = re.search(pattern, sent)
            if m:
                year_str = m.group(1)
                try:
                    yr = chinese_num_to_int(year_str)
                except:
                    try:
                        yr = int(year_str)
                    except:
                        continue
                return resolve_year(dynasty, reign, yr, book_prefix)
    
    # Try emperor + reign_year pattern (前元/中元/后元)
    emperor_reign = re.search(r'(文帝|景帝|武帝|昭帝|宣帝|元帝|成帝|哀帝)[前后中]元([一二三四五六七八九十\d]+)年', sent)
    if emperor_reign:
        emperor = emperor_reign.group(1)
        yr_str = emperor_reign.group(2)
        try:
            yr = chinese_num_to_int(yr_str)
        except:
            yr = 1
        
        # Simplified mapping
        emp_reign_map = {
            '文帝': {'前': -179, '后': -163},
            '景帝': {'前': -156, '中': -149, '后': -143},
            '武帝': {'建元': -140},
        }
        # Just return rough estimate for now
        if emperor in emp_reign_map:
            for key, base in emp_reign_map[emperor].items():
                if key in emperor_reign.group(0):
                    return base + yr - 1
        return None
    
    return None

def extract_date_simple(sent, book_prefix):
    """Try to extract any year number."""
    # General year pattern: [number]年
    m = re.search(r'([一二三四五六七八九十百零\d]+)年', sent)
    if not m:
        return None
    year_str = m.group(1)
    try:
        yr = chinese_num_to_int(year_str)
    except:
        return None
    return yr  # just raw year number as fallback

def chinese_num_to_int(cn_str):
    """Convert Chinese number string to integer."""
    c2n = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000, '万': 10000,
    }
    if cn_str.isdigit():
        return int(cn_str)
    
    result = 0
    temp = 0
    for ch in cn_str:
        if ch in ('百', '千', '万'):
            if temp == 0:
                temp = 1
            result += temp * c2n[ch]
            temp = 0
        elif ch == '十':
            if temp == 0:
                temp = 1
            result += temp * 10
            temp = 0
        else:
            temp = c2n.get(ch, 0)
    result += temp
    return result

def is_theoretical(sent):
    """Filter out theoretical/general statements (not specific events)."""
    theoretical_patterns = [
        r'占[曰云]',
        r'占曰',
        r'经[曰云]',
        r'春秋[二].*[日食]',
        r'凡.*[日食月食]',
        r'所谓',
        r'曰.*之(象|应|占)',
    ]
    for pat in theoretical_patterns:
        if re.search(pat, sent):
            return True
    return False

def main():
    corpus_dir = 'corpus'
    all_events = []
    
    # Process all tagged texts
    for fn in sorted(os.listdir(corpus_dir)):
        if not fn.endswith('_tagged.txt'):
            continue
        
        prefix = fn.split('_')[0]
        if prefix not in BOOK_INFO:
            continue
        
        book_title, chapter_name, author, era = BOOK_INFO[prefix]
        
        with open(os.path.join(corpus_dir, fn), 'r', encoding='utf-8') as f:
            text = f.read()
        
        events = extract_events(text, prefix, book_title, chapter_name)
        
        # Add book metadata to each event
        for ev in events:
            ev['author'] = author
            ev['era'] = era
        
        all_events.extend(events)
        print(f'{book_title:10s} {chapter_name:15s}: {len(events)} events')
    
    print(f'\nTotal events extracted: {len(all_events)}')
    
    # Filter to events with valid years
    with_year = [ev for ev in all_events if ev['year'] is not None and isinstance(ev['year'], (int, float))]
    print(f'Events with year: {len(with_year)}')
    
    # Sort by year
    with_year.sort(key=lambda x: x['year'] if x['year'] else 0)
    
    # Type breakdown
    type_counts = {}
    for ev in all_events:
        t = ev['type']
        type_counts[t] = type_counts.get(t, 0) + 1
    print('\nType breakdown:')
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f'  {t}: {c}')
    
    # Save JSON
    os.makedirs('data', exist_ok=True)
    with open('data/events.json', 'w', encoding='utf-8') as f:
        json.dump(with_year, f, ensure_ascii=False, indent=2)
    print(f'\nSaved {len(with_year)} events to data/events.json')
    
    return with_year

if __name__ == '__main__':
    events = main()
