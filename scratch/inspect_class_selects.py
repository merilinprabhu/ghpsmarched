import re, sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    'Attendance.html',
    'FlnAssessment.html',
    'BridgeCourse.html',
    'HeightWeightTracker.html',
    'UniformDistribution.html',
    'TextbookDistribution.html',
    'EggBananaDistribution.html',
    'ShoeSocksDistribution.html'
]

for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all select elements with class or std in their id/name
    selects = re.findall(r'<select[^>]*id="[^"]*class[^"]*"[^>]*>[\s\S]*?</select>', content, re.IGNORECASE)
    if not selects:
        selects = re.findall(r'<select[^>]*id="[^"]*std[^"]*"[^>]*>[\s\S]*?</select>', content, re.IGNORECASE)
    print(f"=== {fn} ===")
    for s in selects[:2]:
        has_lkg = 'LKG' in s
        has_ukg = 'UKG' in s
        print(f"  Select: Has LKG: {has_lkg}, Has UKG: {has_ukg}")
        for opt in re.findall(r'<option[^>]*>.*?</option>', s)[:5]:
            print(f"    {opt}")
