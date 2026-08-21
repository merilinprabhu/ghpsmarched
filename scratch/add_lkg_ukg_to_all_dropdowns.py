import re, sys

sys.stdout.reconfigure(encoding='utf-8')

def patch_dropdown(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        orig_len = len(code)
        
        # Pattern 1: <option value="1">Class 1</option>
        if '<option value="1">Class 1</option>' in code and '<option value="LKG">LKG</option>' not in code:
            code = code.replace(
                '<option value="1">Class 1</option>',
                '<option value="LKG">LKG</option>\n                      <option value="UKG">UKG</option>\n                      <option value="1">Class 1</option>'
            )
        
        # Pattern 2: <option value="1">1</option>
        if '<option value="1">1</option>' in code and '<option value="LKG">LKG</option>' not in code:
            code = code.replace(
                '<option value="1">1</option>',
                '<option value="LKG">LKG</option>\n                  <option value="UKG">UKG</option>\n                  <option value="1">1</option>'
            )
            
        # Pattern 3: <option value="1">1st Standard</option> or 1st Class
        if '<option value="1">1st Std</option>' in code and '<option value="LKG">LKG</option>' not in code:
            code = code.replace(
                '<option value="1">1st Std</option>',
                '<option value="LKG">LKG</option>\n                  <option value="UKG">UKG</option>\n                  <option value="1">1st Std</option>'
            )

        if len(code) != orig_len:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            print(f"✅ Added LKG & UKG to {filepath}")
        else:
            print(f"ℹ️ No change or already present in {filepath}")
    except Exception as e:
        print(f"❌ Error {filepath}: {e}")

files = [
    'CceAssessmet.html',
    'CceConsolidatedReport.html',
    'CcePartB.html',
    'FlnAssessment.html',
    'BridgeCourse.html',
    'Attendance.html',
    'HeightWeightTracker.html',
    'UniformDistribution.html',
    'TextbookDistribution.html',
    'EggBananaDistribution.html',
    'ShoeSocksDistribution.html'
]

for fp in files:
    patch_dropdown(fp)
