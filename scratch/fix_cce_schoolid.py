import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    cce = f.read()

# Fix all schoolId resolutions in CceAssessmet.html
cce = re.sub(
    r'const schoolId = \(session\?\.user\?\.user_metadata\?\.school_id \|\| localStorage\.getItem\("school_id"\)\)( \|\| null)?;',
    r'const rawSchoolId = (session?.user?.user_metadata?.school_id || localStorage.getItem("school_id")) || null;\n        const schoolId = (rawSchoolId && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(rawSchoolId)) ? rawSchoolId : null;',
    cce
)

with open('CceAssessmet.html', 'w', encoding='utf-8') as f:
    f.write(cce)

print("Sanitized all schoolId in CceAssessmet.html")
