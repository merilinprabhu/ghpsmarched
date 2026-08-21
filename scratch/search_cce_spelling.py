import glob, os, re

files = glob.glob('*.html') + glob.glob('*.js')
print("Searching for CceAssessment vs CceAssessmet in all files...")

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    
    matches_correct = re.findall(r'cceassessment\.html', content, re.IGNORECASE)
    matches_typo = re.findall(r'cceassessmet\.html', content, re.IGNORECASE)
    
    if matches_correct or matches_typo:
        print(f"File: {f}")
        if matches_correct:
            print(f"  [WITH 'n' - CceAssessment.html]: {len(matches_correct)} occurrences")
            for line_no, line in enumerate(content.splitlines(), 1):
                if re.search(r'cceassessment\.html', line, re.IGNORECASE):
                    print(f"    L{line_no}: {line.strip()[:100]}")
        if matches_typo:
            print(f"  [WITHOUT 'n' - CceAssessmet.html]: {len(matches_typo)} occurrences")
            for line_no, line in enumerate(content.splitlines(), 1):
                if re.search(r'cceassessmet\.html', line, re.IGNORECASE):
                    print(f"    L{line_no}: {line.strip()[:100]}")
