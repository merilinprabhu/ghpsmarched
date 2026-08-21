with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for idx, l in enumerate(lines, 1):
    if 'cce' in l.lower():
        safe_l = l.strip()[:140].encode('ascii', errors='replace').decode('ascii')
        print(f"L{idx}: {safe_l}")
