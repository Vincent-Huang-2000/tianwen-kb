#!/usr/bin/env python3
"""Build entity detail page with separate data + app JS files."""
import json

with open('data/entity_index.json','r',encoding='utf-8') as f:
    entities = json.load(f)

BOOK_URLS = {
    '史记·天官书': '../chapters/01_史记_天官书第五.html',
    '汉书·天文志': '../chapters/02_汉书_天文志.html',
    '后汉书·天文志': '../chapters/03_后汉书_天文志.html',
    '晋书·天文志': '../chapters/04_晋书_天文志.html',
    '宋书·天文志': '../chapters/05_宋书_天文志.html',
    '南齐书·天文志': '../chapters/06_南齐书_天文志.html',
    '魏书·天象志': '../chapters/07_魏书_天象志.html',
    '隋书·天文志': '../chapters/08_隋书_天文志.html',
    '旧唐书·天文志': '../chapters/09_旧唐书_天文志.html',
    '新唐书·天文志': '../chapters/10_新唐书_天文志.html',
    '旧五代史·天文志': '../chapters/11_旧五代史_天文志.html',
    '新五代史·司天考': '../chapters/12_新五代史_司天考.html',
    '宋史·天文志': '../chapters/13_宋史_天文志.html',
    '辽史·历象志': '../chapters/14_辽史_历象志.html',
    '金史·天文志': '../chapters/15_金史_天文志.html',
    '元史·天文志': '../chapters/16_元史_天文志.html',
    '明史·天文志': '../chapters/17_明史_天文志.html',
    '步天歌': '../chapters/18_步天歌.html',
    '乙巳占': '../chapters/19_乙巳占.html',
    '星庐·中国古天文学概论': '../chapters/20_星庐中国古天文学概论.html',
}

with open('docs/kg/entity_data.js','w',encoding='utf-8') as f:
    f.write('window.ENTITIES=')
    json.dump(entities, f, ensure_ascii=False)
    f.write(';\nwindow.BOOK_URLS=')
    json.dump(BOOK_URLS, f, ensure_ascii=False)
    f.write(';\n')

entity_html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>实体详情 - 星庐</title>
<link rel="stylesheet" href="../css/style.css">
<style>
body{background:var(--bg-deepest);color:var(--text-body);font-family:var(--font-sans);margin:0}
.c{max-width:800px;margin:0 auto;padding:20px}
h1{color:var(--accent-gold);font-family:var(--font-serif);margin-bottom:4px}
.meta{color:var(--text-muted);font-size:0.85rem;margin-bottom:20px}
.badge{display:inline-block;padding:2px 10px;border-radius:10px;font-size:0.75rem;color:#fff;margin-right:8px}
.section{margin:20px 0}
.section h2{color:var(--accent-gold);font-size:1rem;border-bottom:1px solid var(--border);padding-bottom:6px}
.book-list{display:flex;flex-wrap:wrap;gap:8px}
.book-item{padding:6px 14px;background:var(--bg-card);border:1px solid var(--border);border-radius:6px;font-size:0.82rem;text-decoration:none;color:var(--text-body);transition:all 0.2s}
.book-item:hover{background:var(--accent-gold);color:#0a0e1a}
.book-count{font-weight:700;color:var(--accent-gold);margin-left:4px}
.ctx-item{padding:8px 12px;margin:4px 0;background:var(--bg-card);border:1px solid var(--border);border-radius:4px;font-size:0.82rem;line-height:1.5;display:block;text-decoration:none;color:var(--text-body);transition:all 0.2s}
.ctx-item:hover{background:#1a2240;border-color:var(--accent-gold)}
.ctx-item small{color:var(--accent-gold)}
.notfound{text-align:center;padding:60px;color:var(--text-muted)}
.back{display:inline-block;margin-bottom:16px;color:var(--accent-gold);text-decoration:none;font-size:0.9rem}
.back:hover{text-decoration:underline}
</style>
</head>
<body>
<nav class="top-nav"><div class="nav-inner">
<a href="../index.html" class="nav-logo">&#9737; 星庐</a>
<div class="nav-links"><a href="../index.html">首页</a><a href="../search.html">搜索</a>
<a href="../kg/timeline.html">天象事件</a><a href="../kg/network.html">知识图谱</a></div>
</div></nav>
<div class="c">
<a id="back-link" href="javascript:history.back()" class="back">&#8592; 返回原文</a>
<div id="content"><p class="notfound">加载中...</p></div>
</div>
<script src="entity_data.js"></script>
<script src="entity_app.js"></script>
</body>
</html>'''

with open('docs/kg/entity.html','w',encoding='utf-8') as f:
    f.write(entity_html)
print(f'entity.html: {len(entity_html)} bytes')

entity_app = r'''var COLORS={星:"#FFD700",官:"#7DC2B2",曜:"#F49B8A",象:"#FF6B6B",神:"#C9A96E",州:"#7EB8DA",岁:"#6B8DB5",器:"#D4A574",历:"#B39DDB"};
function esc(s){var d=document.createElement("div");d.textContent=s;return d.innerHTML;}
(function(){
var m=window.location.search.match(/[?&]name=([^&]+)/);
if(!m){document.getElementById("content").innerHTML='<p class="notfound">Missing name</p>';return;}
var name=decodeURIComponent(m[1]),ent=null;
var all=window.ENTITIES||[];
for(var i=0;i<all.length;i++){if(all[i].name===name){ent=all[i];break;}}
if(!ent){document.getElementById("content").innerHTML='<p class="notfound">Not found: '+esc(name)+'</p>';return;}
var URLS=window.BOOK_URLS||{};
var h='<h1>'+esc(ent.name)+'</h1>';
h+='<div class="meta"><span class="badge" style="background:'+(COLORS[ent.type]||"#888")+'">'+ent.type_cn+'</span>';
h+='<strong>'+ent.total+'</strong> occurrences in <strong>'+ent.book_count+'</strong> books</div>';
h+='<div class="section"><h2>Cross-book Distribution</h2><div class="book-list">';
var books=Object.keys(ent.books).sort(function(a,b){return ent.books[b]-ent.books[a]});
books.forEach(function(b){var u=URLS[b]||"#";h+='<a href="'+u+'" class="book-item" target="_blank">'+esc(b)+' <span class="book-count">'+ent.books[b]+'</span></a>'});
h+='</div></div>';
if(ent.contexts&&ent.contexts.length>0){
 h+='<div class="section"><h2>Context (click to jump to source)</h2>';
 ent.contexts.forEach(function(c){
  var txt=typeof c==="string"?c:c.text,bk=typeof c==="string"?"":c.book;
  var chUrl=URLS[bk]||"";
  var findUrl=chUrl+"#find="+encodeURIComponent(name);
  h+='<a href="'+findUrl+'" class="ctx-item">'+esc(txt)+' <small>('+esc(bk||"")+')</small></a>';
 });
 h+='</div>';
}
document.getElementById("content").innerHTML=h;
var rm=window.location.search.match(/[?&]ref=([^&]+)/);
if(rm){var ref=decodeURIComponent(rm[1]),bk=document.getElementById("back-link");if(bk){bk.href="../chapters/"+ref+"#find="+encodeURIComponent(name);bk.textContent="\u2190 Back to "+ref.replace(".html","");}}
})();
'''

with open('docs/kg/entity_app.js','w',encoding='utf-8') as f:
    f.write(entity_app)
print(f'entity_app.js: {len(entity_app)} bytes')
