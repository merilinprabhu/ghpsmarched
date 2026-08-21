import glob, re

files = [
    'LbaAssessment.html',
    'CceAssessmet.html',
    'BridgeCourse.html',
    'FlnAssessment.html',
    'Attendance.html',
    'HeightWeightTracker.html',
    'UniformDistribution.html',
    'ShoeSocksDistribution.html',
    'TextbookDistribution.html',
    'EggBananaDistribution.html'
]

uuid_pattern = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    
    matches = re.findall(r"from\(['\"]admissions['\"]\)[^;]+", c)
    print(f"\n--- {f} ---")
    for m in matches:
        print(" ", m[:150].replace('\n', ' '))
