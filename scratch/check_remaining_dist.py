import re, glob

# Check remaining distribution and tracker files
dist_files = [
    'ShoeTracker.html',
    'ShoeSocksDistribution.html',
    'TextbookDistribution.html',
    'UniformDistribution.html',
    'EggBananaDistribution.html',
    'HeightWeightTracker.html',
    'incentives.html',
    'StudentUpdate.html',
    'ApaarModule.html'
]

for fn in dist_files:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"=== {fn} ===")
    matches = re.findall(r'.{0,50}from\([\'"]admissions[\'"]\).{0,150}', content)
    for m in matches[:3]:
        print("  ", m.strip())
