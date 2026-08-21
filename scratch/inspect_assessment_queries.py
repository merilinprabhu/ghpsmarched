import re, glob

assessment_files = [
    'LbaAssessment.html',
    'CceAssessmet.html',
    'CceConsolidatedReport.html',
    'CcePartB.html',
    'FlnAssessment.html',
    'BridgeCourse.html',
    'Attendance.html',
    'HeightWeightTracker.html',
    'ShoeSocksDistribution.html',
    'TextbookDistribution.html',
    'UniformDistribution.html',
    'EggBananaDistribution.html',
    'incentives.html',
    'StudentUpdate.html',
    'ApaarModule.html'
]

for fn in assessment_files:
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.splitlines()
        print(f"=== {fn} ({len(lines)} lines) ===")
        for idx, line in enumerate(lines):
            if "from('admissions')" in line or 'from("admissions")' in line:
                print(f"  Line {idx+1}: {line.strip()[:100]}")
    except Exception as e:
        print(f"Error {fn}: {e}")
