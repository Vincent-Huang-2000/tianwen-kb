import re
with open(r'D:\24history\twz\星庐中国古天文学概论.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# Line 15 (0-indexed 14): [摘要：\t2](#_Toc231139331)
line = lines[14].rstrip('\n')
print(repr(line[:80]))
m = re.match(r'\[(.+?)(?:\t\d+)?\]\((#_[^)]+)\)', line)
print('Match:', m is not None)
