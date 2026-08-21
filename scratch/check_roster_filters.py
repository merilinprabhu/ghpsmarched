import re, glob, os

files = glob.glob('*.html')
print(f"Total HTML files: {len(files)}")

for f in sorted(files):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()
    if "from('admissions')" in content or 'from("admissions")' in content:
        has_tc_filter = "status" in content and ("TC_OUT" in content or "DELETED" in content)
        has_trashed_filter = "trashed_students_list" in content
        print(f"{f:<30} | Has DB 'from(admissions)': YES | Filters TC_OUT/DELETED: {has_tc_filter} | Filters Trashed: {has_trashed_filter}")
