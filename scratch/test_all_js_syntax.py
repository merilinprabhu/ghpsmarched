import glob, re, subprocess, os

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

for fname in files:
    if not os.path.exists(fname):
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract script blocks without src attribute
    script_matches = re.finditer(r'<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>', content, re.IGNORECASE)
    
    print(f"\n==================== {fname} ====================")
    for idx, match in enumerate(script_matches):
        js_code = match.group(1)
        # Write to temp file and test with node -c
        temp_js = f"scratch/temp_{idx}.js"
        with open(temp_js, 'w', encoding='utf-8') as tf:
            tf.write(js_code)
        
        res = subprocess.run(["node", "-c", temp_js], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[ERROR in script {idx}]: {res.stderr}")
        else:
            print(f"[OK] script {idx} parsed successfully by node.")
