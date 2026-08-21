import re, sys

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>', html, re.IGNORECASE)
main_script = scripts[4]

with open('scratch/cce_extracted.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

print(f"Extracted JS: {len(main_script)} characters, {len(main_script.splitlines())} lines")

# Let's inspect functions and initial execution in main_script
lines = main_script.splitlines()
print("\n--- Last 60 lines of script ---")
for i, line in enumerate(lines[-60:], len(lines)-60+1):
    # safe print
    safe_line = line.encode('ascii', errors='replace').decode('ascii')
    print(f"{i}: {safe_line}")

# Search for window.onload, DOMContentLoaded, or immediate execution
print("\n--- Init / Onload occurrences ---")
for i, line in enumerate(lines):
    if any(k in line for k in ['addEventListener', 'onload', 'initSidebar', 'loadStudents', 'loadAssessment', 'fetchStudents', 'checkAuth']):
        safe_line = line.encode('ascii', errors='replace').decode('ascii')
        print(f"Line {i+1}: {safe_line[:120]}")
