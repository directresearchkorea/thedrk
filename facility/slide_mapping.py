import zipfile, re, os, json
z = zipfile.ZipFile(r'DRK facility.pptx')
slides = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]
slides.sort()
res = []
for s in slides:
    text = ''.join(re.findall(r'<a:t>(.*?)</a:t>', z.read(s).decode('utf-8')))
    rel_file = s.replace('ppt/slides/slide', 'ppt/slides/_rels/slide') + '.rels'
    images = []
    try:
        rel_content = z.read(rel_file).decode('utf-8')
        images = re.findall(r'Target="\.\./media/(.*?)"', rel_content)
    except:
        pass
    res.append({'slide': s, 'text': text[:50], 'images': images})
print(json.dumps(res, indent=2))
