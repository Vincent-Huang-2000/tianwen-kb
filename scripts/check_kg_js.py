with open('docs/kg/network.html','r',encoding='utf-8') as f:
    h=f.read()
print('Script tags:', h.count('<script>'), h.count('</script>'))
s=h.index('<script>')
e=h.index('</script>',s)
js=h[s+8:e]
# Check first chars
print('JS starts:', repr(js[:80]))
print('JS ends:', repr(js[-80:]))
# Check for special chars that break JS in inline scripts
bad = ['</script', '-->', '\u2028', '\u2029']
for b in bad:
    if b in js:
        print('FOUND:', repr(b), 'at', js.index(b))
