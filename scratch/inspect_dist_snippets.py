import re, sys

def patch_file(filepath, search_pattern, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if search_pattern in content:
        new_content = content.replace(search_pattern, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Successfully patched {filepath}")
    else:
        print(f"⚠️ Search pattern not found in {filepath}")

# 1. HeightWeightTracker.html
with open('HeightWeightTracker.html', 'r', encoding='utf-8') as f:
    txt = f.read()
# Let's inspect where studQuery is in HeightWeightTracker.html
m = re.search(r'let studQuery = supabaseClient\.from\(\'admissions\'\)[\s\S]{1,300}\.map\(', txt)
if m:
    print("HeightWeightTracker match found:\n", m.group(0))

# 2. TextbookDistribution.html
with open('TextbookDistribution.html', 'r', encoding='utf-8') as f:
    txt = f.read()
m = re.search(r'studQuery = supabaseClient\.from\(\'admissions\'\)[\s\S]{1,300}\.map\(', txt)
if m:
    print("TextbookDistribution match found:\n", m.group(0))

# 3. UniformDistribution.html
with open('UniformDistribution.html', 'r', encoding='utf-8') as f:
    txt = f.read()
m = re.search(r'let studQuery = supabaseClient\.from\(\'admissions\'\)[\s\S]{1,300}\.map\(', txt)
if m:
    print("UniformDistribution match found:\n", m.group(0))
