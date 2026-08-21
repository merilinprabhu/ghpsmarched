import re

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract all document.getElementById('...') from JS
js_dom_ids = set(re.findall(r'document\.getElementById\([\'"]([a-zA-Z0-9_-]+)[\'"]\)', html))

# Extract all id="..." from HTML
html_ids = set(re.findall(r'\bid=[\'"]([a-zA-Z0-9_-]+)[\'"]', html))

missing_ids = js_dom_ids - html_ids
print(f"Total getElementById queries: {len(js_dom_ids)}")
print(f"Total HTML IDs found: {len(html_ids)}")
print(f"Missing IDs count: {len(missing_ids)}")
print("Missing IDs:")
for mid in sorted(missing_ids):
    # Check if there is null safety in the JS for this ID
    # Find snippets using this ID
    occurrences = [m.start() for m in re.finditer(re.escape(mid), html)]
    print(f"\n--- ID: '{mid}' (used {len(occurrences)} times) ---")
    for pos in occurrences[:5]:
        start = max(0, pos - 50)
        end = min(len(html), pos + 100)
        snippet = html[start:end].replace('\n', ' ')
        print(f"  Snippet: {snippet}")
