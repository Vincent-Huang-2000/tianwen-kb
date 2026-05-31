#!/usr/bin/env python3
import json

with open('data/star_tree.json','r',encoding='utf-8') as f: tree=json.load(f)
with open('data/cross_book_events.json','r',encoding='utf-8') as f: cross=json.load(f)
with open('data/astrology.json','r',encoding='utf-8') as f: astro=json.load(f)

# Use placeholder-based template to avoid quote escaping issues
tmpl = open('scripts/kg_template.html','r',encoding='utf-8').read() if __import__('os').path.exists('scripts/kg_template.html') else None

# Build HTML directly
tree_j = json.dumps(tree,ensure_ascii=False)
cross_j = json.dumps(cross,ensure_ascii=False)  
astro_j = json.dumps(astro,ensure_ascii=False)

html = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
html += '<title>知识图谱 - 星庐</title>\n'
html += '<link rel="stylesheet" href="../css/style.css">\n'
html += '<style>\n'
html += 'body{background:var(--bg-deepest);color:var(--text-body);font-family:var(--font-sans);margin:0}\n'
html += '.main{max-width:1400px;margin:0 auto;padding:20px}\n'
html += 'h1{color:var(--accent-gold);font-family:var(--font-serif);text-align:center;margin-bottom:4px}\n'
html += 'h2{color:var(--accent-gold);font-size:1.1rem;margin:24px 0 12px;border-bottom:1px solid var(--border);padding-bottom:8px}\n'
html += '.tabs{display:flex;gap:0;justify-content:center;margin:16px 0}\n'
html += '.tabs button{padding:10px 24px;border:1px solid var(--border);background:var(--bg-card);color:var(--text-body);cursor:pointer;font-size:0.9rem}\n'
html += '.tabs button:first-child{border-radius:6px 0 0 6px}\n'
html += '.tabs button:last-child{border-radius:0 6px 6px 0}\n'
html += '.tabs button.on{background:var(--accent-gold);color:#0a0e1a;border-color:var(--accent-gold)}\n'
html += '.panel{display:none}.panel.on{display:block}\n'
html += '.tree{font-size:0.85rem;line-height:1.8}\n'
html += '.tree ul{list-style:none;padding-left:24px}\n'
html += '.tree li{position:relative}\n'
html += '.tree li::before{content:"";position:absolute;left:-16px;top:10px;width:12px;height:1px;background:var(--border)}\n'
html += '.tree li::after{content:"";position:absolute;left:-16px;top:0;bottom:0;width:1px;background:var(--border)}\n'
html += '.tree li:last-child::after{height:10px}\n'
html += '.tree .node{cursor:pointer;color:var(--text-body);transition:color 0.2s;display:inline-block;padding:2px 6px;border-radius:4px}\n'
html += '.tree .node:hover{color:var(--accent-gold);background:rgba(201,169,110,0.1)}\n'
html += '.tree .node.folder{font-weight:600;color:var(--accent-warm)}\n'
html += '.tree .node.desc{font-size:0.75rem;color:var(--text-muted);margin-left:8px}\n'
html += '.tree .collapsed>ul{display:none}\n'
html += '.tag-canglong{background:rgba(74,155,142,0.2);color:#4a9b8e}\n'
html += '.tag-zhuque{background:rgba(196,107,90,0.2);color:#c46b5a}\n'
html += '.tag-baihu{background:rgba(196,163,90,0.2);color:#c4a35a}\n'
html += '.tag-xuanwu{background:rgba(107,141,181,0.2);color:#6b8db5}\n'
html += '.xb-item{padding:12px 16px;margin-bottom:8px;background:var(--bg-card);border:1px solid var(--border);border-radius:6px}\n'
html += '.xb-head{display:flex;align-items:center;gap:12px;margin-bottom:6px}\n'
html += '.xb-year{font-weight:700;color:var(--accent-gold);min-width:70px}\n'
html += '.xb-type{padding:2px 10px;border-radius:10px;font-size:0.75rem;color:#fff}\n'
html += '.xb-sources{font-size:0.75rem;color:var(--text-muted)}\n'
html += '.xb-text{font-size:0.82rem;line-height:1.6;color:var(--text-muted);padding-left:22px}\n'
html += '.xb-link{text-decoration:none;display:block}\n'
html += '.xb-link:hover .xb-text{color:var(--accent-gold)}\n'
html += '.xb-omen{color:var(--accent-gold);font-size:0.78rem;display:inline-block;margin-top:2px}\n'
html += '.as-item{padding:10px 14px;margin-bottom:6px;background:var(--bg-card);border:1px solid var(--border);border-radius:6px;display:flex;gap:12px;align-items:flex-start}\n'
html += '.as-type{min-width:60px;padding:2px 8px;border-radius:10px;font-size:0.72rem;color:#fff;text-align:center}\n'
html += '.as-consequence{font-size:0.82rem;line-height:1.5;flex:1}\n'
html += '.as-source{font-size:0.7rem;color:var(--text-muted)}\n'
html += '.e-solar{background:#B33A3A}.e-lunar{background:#5B3A7A}.e-comet{background:#3A6B5A}\n'
html += '.e-meteor{background:#7A5B3A}.e-encroach{background:#8B4513}\n'
html += '</style>\n</head>\n<body>\n'

# Nav
html += '<nav class="top-nav"><div class="nav-inner">\n'
html += '<a href="../index.html" class="nav-logo">&#9737; 星庐</a>\n'
html += '<div class="nav-links">\n'
html += '<a href="../index.html">首页</a><a href="../search.html">搜索</a>\n'
html += '<a href="../kg/timeline.html">天象事件</a><a href="../kg/starmap.html">古星图</a>\n'
html += '<a href="../kg/network.html">知识图谱</a></div>\n'
html += '</div></nav>\n'

# Main content
html += '<div class="main">\n'
html += '<h1>知识图谱</h1>\n'

# Tabs
html += '<div class="tabs">\n'
html += '<button class="on" onclick="showTab(\'tree\')">星官谱系</button>\n'
html += '<button onclick="showTab(\'cross\')">跨书关联 (' + str(len(cross)) + ')</button>\n'
html += '<button onclick="showTab(\'astro\')">占星对应 (' + str(len(astro)) + ')</button>\n'
html += '</div>\n'

# Tree panel
html += '<div class="panel on" id="panel-tree">\n'
html += '<h2>中国星官体系 · 三垣二十八宿</h2>\n'
html += '<div class="tree" id="tree"></div>\n</div>\n'

# Cross panel
html += '<div class="panel" id="panel-cross">\n'
html += '<h2>跨书天象验证</h2>\n'
html += '<p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:16px">同一天象在不同史书中的独立记载，共 ' + str(len(cross)) + ' 组</p>\n'
html += '<div id="cross-list"></div>\n</div>\n'

# Astro panel
html += '<div class="panel" id="panel-astro">\n'
html += '<h2>占星对应关系</h2>\n'
html += '<p style="color:var(--text-muted);font-size:0.85rem;margin-bottom:16px">天象 → 人事映射规律，共 ' + str(len(astro)) + ' 条</p>\n'
html += '<div id="astro-list"></div>\n</div>\n'

html += '</div>\n'

# JavaScript
html += '<script>\n'
html += 'var treeData=' + tree_j + ';\n'
html += 'var crossData=' + cross_j + ';\n'
html += 'var astroData=' + astro_j + ';\n'

# JS code block
js_code = '''
var tNames={solar_eclipse:"日食",lunar_eclipse:"月食",comet:"彗星",meteor:"流星",guest_star:"客星",encroach:"星犯",guard:"星守",occult:"星掩",entry:"星入",conjunction:"星合",clustering:"星聚",day_visible:"昼见"};
var clsMap={solar_eclipse:"e-solar",lunar_eclipse:"e-lunar",comet:"e-comet",meteor:"e-meteor",encroach:"e-encroach"};

function showTab(name){
  document.querySelectorAll(".tabs button").forEach(function(b){b.classList.remove("on")});
  event.target.classList.add("on");
  document.querySelectorAll(".panel").forEach(function(p){p.classList.remove("on")});
  document.getElementById("panel-"+name).classList.add("on");
}

function renderTree(node,container,depth){
  var ul=document.createElement("ul");
  container.appendChild(ul);
  (node.children||[]).forEach(function(child){
    var li=document.createElement("li");
    var span=document.createElement("span");
    span.className="node";
    if(child.children&&child.children.length>0){
      span.className+=" folder";
      span.textContent=(depth===0?"\u25cf ":"")+child.name;
      if(child.description){
        var d=document.createElement("span");d.className="node desc";d.textContent=" \u2014 "+child.description;span.appendChild(d);
      }
      span.onclick=function(e){e.stopPropagation();this.parentElement.classList.toggle("collapsed");};
      li.appendChild(span);
      renderTree(child,li,depth+1);
    } else {
      span.textContent=child.name;
      if(child.description){
        var d=document.createElement("span");d.className="node desc";d.textContent=" \u2014 "+child.description;span.appendChild(d);
      }
      if(child.stars){
        var s=document.createElement("span");s.className="node desc";s.textContent=" \u2605 "+child.stars;span.appendChild(s);
      }
      li.appendChild(span);
    }
    ul.appendChild(li);
  });
}

function esc(s){var d=document.createElement("div");d.textContent=s;return d.innerHTML;}

// Render tree
renderTree(treeData,document.getElementById("tree"),0);

// Render cross-book
var cl=document.getElementById("cross-list");
crossData.forEach(function(cb){
  var y=cb.year<0?"\u524d"+(-cb.year):""+cb.year;
  var h="<div class=\\"xb-item\\">";
  h+="<div class=\\"xb-head\\"><span class=\\"xb-year\\">"+y+"</span><span class=\\"xb-type "+(clsMap[cb.type]||"")+"\\">"+(tNames[cb.type]||cb.type)+"</span><span class=\\"xb-sources\\">"+cb.sources.length+"部史书："+cb.sources.join(", ")+"</span></div>";
  cb.events.slice(0,3).forEach(function(ev){
    h+="<div class=\"xb-text\" data-url=\""+(ev.url||"")+"\" onclick=\"if(this.dataset.url)window.open(this.dataset.url,'_blank')\" style=\"cursor:pointer\">"+esc(ev.description)+" <small>("+ev.source+")</small>";
    if(ev.omen) h+=" <span class=\"xb-omen\">"+esc(ev.omen)+"</span>";
    h+="</div>";
  });
  h+="</div>";
  cl.innerHTML+=h;
});

// Render astrology
var al=document.getElementById("astro-list");
astroData.forEach(function(a){
  var h="<div class=\\"as-item\\">";
  h+="<span class=\\"as-type "+(clsMap[a.type]||"")+"\\">"+(tNames[a.type]||a.type)+"</span>";
  h+="<div class=\\"as-consequence\\">"+esc(a.consequence)+"</div>";
  h+="<div class=\\"as-source\\">"+a.source+"</div>";
  h+="</div>";
  al.innerHTML+=h;
});
'''
html += js_code + '\n</script>\n</body>\n</html>'

with open('docs/kg/network.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Saved network.html: {len(html):,} bytes')
