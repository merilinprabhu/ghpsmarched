import glob, re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<a\s+[^>]*href=[\'"][^\'"]*cce[^\'"]*[\'"][^>]*>[\s\S]*?</a>', text, re.IGNORECASE)
print(f"CCE links in dashboard.html ({len(matches)}):")
for m in matches:
    print(m.strip()[:150])

matches_onclick = re.findall(r'window\.location\.href\s*=\s*[\'"][^\'"]*cce[^\'"]*[\'"]', text, re.IGNORECASE)
print(f"\nCCE window.location in dashboard.html ({len(matches_onclick)}):")
for m in matches_onclick:
    print(m.strip())
