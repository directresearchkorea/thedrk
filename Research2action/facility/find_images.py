import zipfile, re
z = zipfile.ZipFile(r'DRK facility.pptx')
for f in z.namelist():
    if f.endswith('.rels'):
        text = z.read(f).decode('utf-8')
        images = re.findall(r'Target="\.\./media/(.*?)"', text)
        if images:
            print(f, images)
