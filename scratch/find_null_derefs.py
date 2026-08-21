import re

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect everything from script line 1 to 200
with open('scratch/cce_extracted.js', 'r', encoding='utf-8') as f:
    js = f.read()

lines = js.splitlines()

# Search for potential runtime errors:
# 1. document.getElementById(...) without null checks
# 2. variables used before declaration
# 3. undefined function calls

for i, l in enumerate(lines):
    # check for document.getElementById where null dereference can occur
    if 'document.getElementById' in l:
        # e.g. document.getElementById('foo').classList... without ?. or if check
        m = re.findall(r'document\.getElementById\([\'"]([^\'"]+)[\'"]\)\.([a-zA-Z]+)', l)
        for target_id, prop in m:
            if target_id not in html:
                print(f"CRITICAL: Line {i+1} accesses .{prop} on non-existent element '{target_id}'!")
                print(f"   Code: {l.strip()}")
