import re

with open('insights/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace filter buttons with a placeholder
content = re.sub(r'<div class="insights-filter reveal" id="insight-filter">.*?</div>', '<!-- INSIGHTS_FILTER -->', content, flags=re.DOTALL)

# Replace grid with a placeholder
content = re.sub(r'<div class="insights-grid" id="insights-grid">.*?</div>\s*<div id="insights-empty"', '<!-- INSIGHTS_GRID -->\n    <div id="insights-empty"', content, flags=re.DOTALL)

with open('tools/insights-template.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Template created.')
