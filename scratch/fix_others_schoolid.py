import re, sys

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['BridgeCourse.html', 'LbaAssessment.html', 'FlnAssessment.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        code = f.read()

    code = re.sub(
        r'const schoolId = \(session\?\.user\?\.user_metadata\?\.school_id \|\| localStorage\.getItem\("school_id"\)\)( \|\| null)?;',
        r'const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;\n        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;',
        code
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(code)

    print(f"Sanitized all schoolId in {fname}")
