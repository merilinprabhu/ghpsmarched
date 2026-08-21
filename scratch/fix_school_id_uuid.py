import glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')

files = [
    'CceAssessmet.html',
    'BridgeCourse.html',
    'LbaAssessment.html',
    'FlnAssessment.html',
    'Attendance.html',
    'HeightWeightTracker.html',
    'UniformDistribution.html',
    'ShoeSocksDistribution.html',
    'TextbookDistribution.html',
    'EggBananaDistribution.html'
]

for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace schoolId checks with isValidUUID check
    # Pattern 1: query = query.or(`school_id.eq.${schoolId},school_id.is.null`);
    p1 = r'if\s*\(\s*schoolId\s*\)\s*\{\s*query\s*=\s*query\.or\(`school_id\.eq\.\$\{schoolId\},school_id\.is\.null`\);\s*\}'
    r1 = r'const isValidUUID = schoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(schoolId);\n        if (isValidUUID) {\n          query = query.or(`school_id.eq.${schoolId},school_id.is.null`);\n        }'
    content = re.sub(p1, r1, content)

    # Pattern 2: if (schoolId) query = query.eq('school_id', schoolId);
    p2 = r'if\s*\(\s*schoolId\s*\)\s*\{\s*query\s*=\s*query\.eq\([\'"]school_id[\'"],\s*schoolId\);\s*\}'
    r2 = r'const isValidUUID = schoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(schoolId);\n        if (isValidUUID) {\n          query = query.eq("school_id", schoolId);\n        }'
    content = re.sub(p2, r2, content)

    # Pattern 3: .eq('school_id', currentSchoolId)
    p3 = r'const\s+currentSchoolId\s*=\s*localStorage\.getItem\([\'"]school_id[\'"]\)\s*\|\|\s*null;'
    r3 = r'let rawSchoolId = localStorage.getItem("school_id") || null;\n    const currentSchoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;'
    content = re.sub(p3, r3, content)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Patched school_id UUID validation in {fname}")
