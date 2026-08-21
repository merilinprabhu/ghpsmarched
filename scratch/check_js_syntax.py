import glob, re

files = glob.glob('*.html')

print("Found HTML files:", files)

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script tags
    scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>', content, re.IGNORECASE)
    print(f"\n--- {fname} ({len(scripts)} scripts) ---")
    
    # Check for unclosed template literals, backticks, syntax issues, mismatched brackets in scripts
    for i, s in enumerate(scripts):
        # Basic bracket counter
        counts = {'{': 0, '}': 0, '(': 0, ')': 0, '[': 0, ']': 0}
        for ch in s:
            if ch in counts:
                counts[ch] += 1
        if counts['{'] != counts['}']:
            print(f"  [!] Script {i}: Curly braces mismatch! {{: {counts['{']}, }}: {counts['}']}}")
        if counts['('] != counts[')']:
            print(f"  [!] Script {i}: Parentheses mismatch! (: {counts['(']}, ): {counts[')']}}")
        if counts['['] != counts[']']:
            print(f"  [!] Script {i}: Square brackets mismatch! [: {counts['[']}, ]: {counts[']']}}")
