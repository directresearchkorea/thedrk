import os

ga_script = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K406SG5L11"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-K406SG5L11');
</script>
</head>"""

base_dir = r'C:\Users\ggamy\OneDrive\Desktop\H_uxrplayer.com'

count = 0
for root, dirs, files in os.walk(base_dir):
    if '.git' in root: continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'G-K406SG5L11' not in content and '</head>' in content:
                    content = content.replace('</head>', ga_script)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    count += 1
            except Exception as e:
                pass

print(f'Total files updated: {count}')
