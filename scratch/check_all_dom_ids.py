import glob, re, os

pages = [
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

print("=== CHECKING ALL PAGES FOR MISSING DOM ELEMENTS REFERENCED IN JS ===")

for p in pages:
    if not os.path.exists(p):
        print(f"File not found: {p}")
        continue
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all document.getElementById('...') in JS
    ids_in_js = set(re.findall(r"document\.getElementById\(['\"]([^'\"]+)['\"]\)", html))
    
    # Find all id="..." in HTML
    ids_in_dom = set(re.findall(r'id=["\']([^"\']+)["\']', html))
    
    # Dynamic IDs like ${student.id} or card-xxx
    missing = []
    for jid in ids_in_js:
        if '$' in jid or '+' in jid:
            continue
        if jid not in ids_in_dom:
            missing.append(jid)
    
    print(f"\n--- {p} ---")
    print(f"  Total JS getElementById IDs: {len(ids_in_js)}")
    print(f"  Total DOM IDs: {len(ids_in_dom)}")
    if missing:
        print(f"  [MISSING DOM IDs referenced in JS]: {missing}")
    else:
        print("  [OK] All static IDs found in DOM.")
