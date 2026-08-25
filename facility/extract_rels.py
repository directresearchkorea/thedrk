import zipfile, re, os, json
z = zipfile.ZipFile(r'DRK facility.pptx')
rels = [f for f in z.namelist() if f.startswith('ppt/slides/_rels/') and f.endswith('.xml.rels')]
rels.sort()
res = {}
for r in rels:
    content = z.read(r).decode('utf-8')
    images = re.findall(r'Target="\.\./media/(.*?)"', content)
    res[os.path.basename(r)] = images
print(json.dumps(res, indent=2))
