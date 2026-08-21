import re, glob

# Check remaining distribution and tracker files
dist_files = [
    'HeightWeightTracker.html',
    'ShoeSocksDistribution.html',
    'TextbookDistribution.html',
    'UniformDistribution.html',
    'EggBananaDistribution.html',
    'incentives.html',
    'StudentUpdate.html',
    'ApaarModule.html'
]

for fn in dist_files:
    with open(fn, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if this file has admissions query
    if "from('admissions')" in content or 'from("admissions")' in content:
        # Check if it filters TC_OUT
        has_filter = 'TC_OUT' in content and 'DELETED' in content
        print(f"{fn:<30} | Has TC_OUT filter: {has_filter}")
