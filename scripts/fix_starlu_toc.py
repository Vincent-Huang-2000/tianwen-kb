import re

path = r"D:\24history\twz\tianwen-kb\docs\chapters\20_星庐中国古天文学概论.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the TOC block: from '<p>\n目 录\n</p>' to the closing '</p>' before '摘要：'
old_start = content.find('<p>\n目 录\n</p>')
if old_start == -1:
    print("TOC not found!")
    exit()

# Find the end - after the TOC, before the actual content '<p>\n摘要：'
old_end = content.find('<p>\n摘要：', old_start)
if old_end == -1:
    print("End of TOC not found!")
    exit()

# The TOC content to remove
old_toc = content[old_start:old_end]

new_toc = '''<div class="toc-nav">
<div class="toc-title">目 录</div>
<ul class="toc-list">
<li class="toc-item"><a href="#abstract">摘要</a></li>
<li class="toc-item"><a href="#intro">引言</a></li>
<li class="toc-item"><a href="#ch1">第一章 太乙观星法的基础原理</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch1-1">1.1 北天极太一：天文学原点与人文投射</a></li>
<li class="toc-item toc-h3"><a href="#ch1-2">1.2 东皇太一：南北整合观测下太阳与太一的恒定性</a></li>
<li class="toc-item toc-h3"><a href="#ch1-3">1.3 六合天象与天地盘架构：日月合朔与北斗斗建的空间对应</a></li>
<li class="toc-item toc-h3"><a href="#ch1-4">1.4 赤道坐标系与两套坐标体系的并存</a></li>
</ul></li>
<li class="toc-item"><a href="#ch2">第二章 十二星次、十二岁阴与斗建太岁</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch2-1">2.1 十二星次的综合定义：大火星授时、岁星纪年与日月合朔</a></li>
<li class="toc-item toc-h3"><a href="#ch2-2">2.2 十二岁阴：北斗斗建与岁阴名称的对应</a></li>
<li class="toc-item toc-h3"><a href="#ch2-3">2.3 斗建太岁：日木相会与北斗所指的六合关系</a></li>
<li class="toc-item toc-h3"><a href="#ch2-4">2.4 辰空、岁空、接辰、小超辰与大超辰——实星纪年的历法修正机制</a></li>
<li class="toc-item toc-h3"><a href="#ch2-5">2.5 实证分析：《吕氏春秋》"岁在涒滩"与《离骚》"摄提贞于孟陬"</a></li>
</ul></li>
<li class="toc-item"><a href="#ch3">第三章 月相纳甲与十天干的天文原理</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch3-1">3.1 《史记·历书甲子篇》的岁阳岁阴纪年体系</a></li>
<li class="toc-item toc-h3"><a href="#ch3-2">3.2 月相六卦：震兑乾巽艮坤的纳甲星象</a></li>
<li class="toc-item toc-h3"><a href="#ch3-3">3.3 月朝与月夕：太阳与月亮相对位置的两组观测</a></li>
<li class="toc-item toc-h3"><a href="#ch3-4">3.4 十天干的星象起源：从月相纳甲到岁阳名称</a></li>
<li class="toc-item toc-h3"><a href="#ch3-5">3.5 十天干的天文历算：366.17天周期与甲子年、庚辰年的星图验证</a></li>
<li class="toc-item toc-h3"><a href="#ch3-6">3.6 戊己纳甲与火运经天的初步探讨</a></li>
</ul></li>
<li class="toc-item"><a href="#ch4">第四章 五运六气的天文原理</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch4-1">4.1 《黄帝内经》七篇大论中的五运六气框架</a></li>
<li class="toc-item toc-h3"><a href="#ch4-2">4.2 五运经天图的逐条天文验证</a>
<ul class="toc-list">
<li class="toc-item toc-h4"><a href="#ch4-2-1">4.2.1 木运经天（丁壬合木）——苍天之气经于危室柳鬼</a></li>
<li class="toc-item toc-h4"><a href="#ch4-2-2">4.2.2 土运经天（甲己合土）——黅天之气经于心尾己分</a></li>
<li class="toc-item toc-h4"><a href="#ch4-2-3">4.2.3 金运经天（乙庚合金）——素天之气经于亢氐昴毕</a></li>
<li class="toc-item toc-h4"><a href="#ch4-2-4">4.2.4 水运经天（丙辛合水）——玄天之气经于张翼娄胃</a></li>
</ul></li>
<li class="toc-item toc-h3"><a href="#ch4-3">4.3 五运经天的统一公式</a></li>
</ul></li>
<li class="toc-item"><a href="#ch5">第五章 六气司天、月相纳甲与先天八卦</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch5-1">5.1 六气司天的十二地支六冲配置</a></li>
<li class="toc-item toc-h3"><a href="#ch5-2">5.2 月相六卦对应三阴三阳</a></li>
<li class="toc-item toc-h3"><a href="#ch5-3">5.3 开阖枢理论与月朝月夕的阴阳升降路径</a></li>
<li class="toc-item toc-h3"><a href="#ch5-4">5.4 刑冲相位：太乙观星法下的六气司天验证</a></li>
<li class="toc-item toc-h3"><a href="#ch5-5">5.5 从月相六气图到先天八卦：120°旋转与坎离水火局</a></li>
<li class="toc-item toc-h3"><a href="#ch5-6">5.6 批判"后世错误月相卦气图"（见图27）</a></li>
</ul></li>
<li class="toc-item"><a href="#ch6">第六章 武王伐纣天象的整合考证</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch6-1">6.1 既有研究的批判：江晓原、钮卫星与夏商周断代工程的局限</a></li>
<li class="toc-item toc-h3"><a href="#ch6-2">6.2 "星在天鼋"新解：大火星（心宿二）的天命象征</a></li>
<li class="toc-item toc-h3"><a href="#ch6-3">6.3 "辰在斗柄"的地盘解读：地支辰（角亢大角）加临斗宿</a></li>
<li class="toc-item toc-h3"><a href="#ch6-4">6.4 "星与日、辰之位皆在北维"的天人感应结构</a></li>
<li class="toc-item toc-h3"><a href="#ch6-5">6.5 "岁在鹑火"的校正：日木相会定义唯一岁次</a></li>
<li class="toc-item toc-h3"><a href="#ch6-6">6.6 七重星象的逐日验证：锁定公元前1047年11月26-27日</a></li>
<li class="toc-item toc-h3"><a href="#ch6-7">6.7 兵阴阳旁证：太岁方位与"背者强"</a></li>
<li class="toc-item toc-h3"><a href="#ch6-8">6.8 与工程及江、钮结论的比较（见图表4）</a></li>
</ul></li>
<li class="toc-item"><a href="#ch7">第七章 结论与展望</a>
<ul class="toc-list">
<li class="toc-item toc-h3"><a href="#ch7-1">7.1 主要学术贡献</a></li>
<li class="toc-item toc-h3"><a href="#ch7-2">7.2 方法的局限性与留白问题</a></li>
<li class="toc-item toc-h3"><a href="#ch7-3">7.3 未来研究方向</a></li>
</ul></li>
</ul>
</div>
'''

# Replace old TOC block with new TOC
content = content.replace(old_toc, new_toc, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK - replaced TOC ({len(old_toc)} -> {len(new_toc)} chars)")
