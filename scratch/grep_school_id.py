with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'school_id' in l:
        print(f"Line {i+1}: {l.strip()}")
