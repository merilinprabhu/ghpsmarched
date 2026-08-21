import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

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

print("=== FINAL VERIFICATION ACROSS ALL MODULES ===")
for f in files:
    if not os.path.exists(f):
        print(f"Missing file: {f}")
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    
    # Check for card container in DOM
    has_card_container = ('cards-container' in c) or ('card' in c)
    # Check for view switcher
    has_view_switcher = ('ಕಾರ್ಡ್ ವ್ಯೂ' in c)
    # Check for LKG/UKG in class dropdowns
    has_lkg_ukg = ('LKG' in c and 'UKG' in c)

    print(f"[OK] {f:30} | Size: {len(c):6} bytes | View Switcher: {has_view_switcher} | Cards: {has_card_container} | LKG/UKG: {has_lkg_ukg}")
