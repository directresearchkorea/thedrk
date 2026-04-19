import os
from bs4 import BeautifulSoup

html_files = [
    'index.html',
    'about/index.html',
    'contact/index.html',
    'services/consumer-research/index.html',
    'services/user-research/index.html',
    'services/research-facility/index.html'
]

templates = ['tools/insights-template.html', 'tools/post-template.html']

def patch_html(filepath):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath}, does not exist")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Add scripts before </body>
    body = soup.find('body')
    if body:
        if not soup.find('script', src='/js/i18n.js'):
            # create tags
            t1 = soup.new_tag('script', src='/js/translations.js')
            t2 = soup.new_tag('script', src='/js/i18n.js')
            t3 = soup.new_tag('script', src='/js/cookie-consent.js')
            
            body.append(t1)
            body.append(t2)
            body.append(t3)

    # 2. Add language switcher to nav
    nav_inner = soup.find('div', class_='nav__inner')
    if nav_inner and not soup.find(id='lang-switcher'):
        switcher_html = """
        <div class="lang-switcher-container">
          <select id="lang-switcher" class="lang-switcher-select">
            <option value="en">EN</option>
            <option value="ko">KO</option>
            <option value="ja">JA</option>
            <option value="zh">ZH</option>
          </select>
        </div>
        """
        switcher_soup = BeautifulSoup(switcher_html, 'html.parser')
        
        cta = nav_inner.find('a', class_='nav__cta')
        if cta:
            cta.insert_before(switcher_soup)

    # 3. Add data-i18n to nav links
    for a in soup.find_all('a', class_='nav__link'):
        text = a.text.strip()
        if text == 'Home': a['data-i18n'] = 'nav_home'
        elif text == 'About': a['data-i18n'] = 'nav_about'
        elif text == 'Insights': a['data-i18n'] = 'nav_insights'
        elif text == 'Services': a['data-i18n'] = 'nav_services'

    for a in soup.find_all('a', class_='nav__cta'):
        text = a.text.strip()
        if text == 'Send RFQ': a['data-i18n'] = 'nav_rfq'
        
    for a in soup.find_all('a', class_='nav__mobile-link'):
        text = a.text.strip()
        if text == 'Home': a['data-i18n'] = 'nav_home'
        elif text == 'About': a['data-i18n'] = 'nav_about'
        elif text == 'Insights': a['data-i18n'] = 'nav_insights'
        elif text == 'Services': a['data-i18n'] = 'nav_services'
        elif text == 'Send RFQ': a['data-i18n'] = 'nav_rfq'

    # Add to specific hero elements if present
    for label in soup.find_all('div', class_='hero__label'):
        if 'Marketing Research Since 2015' in label.text:
            # We don't overwrite the dot, so we set the attribute and in translation we don't include dot, 
            # actually our translation replaces innerHTML. Let's make sure the dot is preserved in translation dict.
            label['data-i18n'] = 'hero_label'
            
    for title in soup.find_all('h1', class_='hero__title'):
        title['data-i18n'] = 'hero_title'
        
    for subtitle in soup.find_all('p', class_='hero__subtitle'):
        subtitle['data-i18n'] = 'hero_subtitle'
        
    for btn in soup.find_all('a', class_='btn--secondary'):
        if btn.text.strip() == 'Our Services':
            btn['data-i18n'] = 'btn_our_services'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f'Patched {filepath}')

for f in html_files + templates:
    patch_html(f)
