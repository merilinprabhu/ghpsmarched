import glob, re

for f in ['dashboard.html', 'StudentList.html', 'FlnAssessment.html', 'LbaAssessment.html', 'BridgeCourse.html', 'CceAssessmet.html', 'Attendance.html']:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    
    m = re.findall(r'if\s*\(!session\)\s*\{[\s\S]*?\}', c)
    print(f"File {f}:")
    for match in m:
        print(" ", match.replace('\n', ' '))
