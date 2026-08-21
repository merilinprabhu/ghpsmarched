import urllib.request
import json
import csv
import io
import re
import sys

# Set stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch Supabase admissions
url = 'https://gsayvnnnfrrkwdfwocbu.supabase.co/rest/v1/admissions?select=*'
headers = {
    'apikey': 'sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS',
    'Authorization': 'Bearer sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    supabase_data = json.loads(resp.read().decode('utf-8'))

print(f"Total Supabase admissions records: {len(supabase_data)}")

# 2. Fetch Google Sheet STS CSV
sheet_url = 'https://docs.google.com/spreadsheets/d/1awYBM024orzUascz9uTYIeXg6rN55sbSJj7hIrhMWp8/gviz/tq?tqx=out:csv&gid=1852377268'
req_sheet = urllib.request.Request(sheet_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_sheet) as resp:
    sheet_csv_text = resp.read().decode('utf-8')

reader = csv.reader(io.StringIO(sheet_csv_text))
sheet_rows = list(reader)
print(f"Total Sheet rows: {len(sheet_rows)}")
print("Header row:", sheet_rows[0])

# Helper functions
def normalize_class(val):
    if not val:
        return ''
    s = str(val).upper().strip()
    if 'LKG' in s: return 'LKG'
    if 'UKG' in s: return 'UKG'
    for n in range(10, 0, -1):
        if s == str(n) or f'CLASS {n}' in s or f'CLASS-{n}' in s or f'{n}TH' in s or f'{n}ST' in s or f'{n}ND' in s or f'{n}RD' in s or f'STD {n}' in s or f'STANDARD {n}' in s:
            return str(n)
    m = re.search(r'\b(10|[1-9])\b', s)
    if m: return m.group(1)
    return s

def clean_sts(val):
    if not val: return ''
    digits = re.sub(r'\D', '', str(val))
    return digits

def normalize_gender(val):
    if not val: return ''
    s = str(val).strip().upper()
    if s.startswith('B') or s.startswith('M') or 'ಗಂಡು' in s or 'BOY' in s or 'MALE' in s:
        return 'Boy'
    if s.startswith('G') or s.startswith('F') or 'ಹೆಣ್ಣು' in s or 'GIRL' in s or 'FEMALE' in s:
        return 'Girl'
    return val

# Parse STS students accurately with exact column mapping
# 0: Sr. No., 1: Enrollment No, 2: Student Name, 3: Father Name, 4: Date of Birth, 5: SocialCategory, 6: Standard, 7: Medium, 8: Gender, 9: Grade Group, 10: Kannada Name, 11: Kannada Father Name
sts_students = []
for i in range(1, len(sheet_rows)):
    r = sheet_rows[i]
    if not r or len(r) < 3: continue
    raw_sts = str(r[1]).strip() if len(r) > 1 else ''
    raw_name = str(r[2]).strip() if len(r) > 2 else ''
    if not raw_sts and not raw_name: continue
    if 'TOTAL' in raw_name.upper() or 'STUDENT NAME' in raw_name.upper() or 'STS' in raw_sts.upper(): continue

    c_sts = clean_sts(raw_sts)
    father = str(r[3]).strip() if len(r) > 3 else ''
    dob = str(r[4]).strip() if len(r) > 4 else ''
    caste = str(r[5]).strip() if len(r) > 5 else ''
    s_class = normalize_class(r[6] if len(r) > 6 else '')
    medium = str(r[7]).strip() if len(r) > 7 else ''
    gender = normalize_gender(r[8] if len(r) > 8 else '')
    name_kn = str(r[10]).strip() if len(r) > 10 else ''
    father_kn = str(r[11]).strip() if len(r) > 11 else ''

    sts_students.append({
        'idx': len(sts_students) + 1,
        'sts': c_sts,
        'raw_sts': raw_sts,
        'name': raw_name,
        'name_kn': name_kn,
        'father': father,
        'father_kn': father_kn,
        'class': s_class,
        'gender': gender,
        'dob': dob,
        'caste': caste,
        'medium': medium
    })

print(f"Parsed STS Master List count: {len(sts_students)}")

# Map Supabase admissions by clean STS and clean name
sb_by_sts = {}
sb_by_name = {}
for stu in supabase_data:
    st_sts = clean_sts(stu.get('student_sts') or stu.get('sts_no') or stu.get('enrolment_no') or '')
    if st_sts:
        sb_by_sts[st_sts] = stu
    name_eng = (stu.get('name_english') or stu.get('student_name') or '').strip().upper()
    if name_eng:
        sb_by_name[name_eng] = stu

# Match STS students against Supabase
matched_by_sts = []
matched_by_name = []
unmatched_sts = []

for s in sts_students:
    sts_num = s['sts']
    name_upper = s['name'].strip().upper()
    if sts_num and sts_num in sb_by_sts:
        matched_by_sts.append((s, sb_by_sts[sts_num]))
    elif name_upper and name_upper in sb_by_name:
        matched_by_name.append((s, sb_by_name[name_upper]))
    else:
        unmatched_sts.append(s)

print(f"\n--- MATCHING RESULTS ---")
print(f"Matched by STS ID: {len(matched_by_sts)}")
print(f"Matched by Name: {len(matched_by_name)}")
print(f"Total STS students matching in Site DB: {len(matched_by_sts) + len(matched_by_name)} / {len(sts_students)}")
print(f"Unmatched (Missing in DB): {len(unmatched_sts)}")

if unmatched_sts:
    print("\n--- UNMATCHED STS STUDENTS (Not found in Supabase DB) ---")
    for u in unmatched_sts:
        print(f"  STS: {u['sts']:12} | Name: {u['name']:25} | Class: {u['class']:3} | Father: {u['father']}")

# Check Supabase students not in STS list
sts_set_numbers = {s['sts'] for s in sts_students if s['sts']}
sts_set_names = {s['name'].strip().upper() for s in sts_students if s['name']}

sb_missing_in_sts = []
for stu in supabase_data:
    st_sts = clean_sts(stu.get('student_sts') or stu.get('sts_no') or stu.get('enrolment_no') or '')
    st_name = (stu.get('name_english') or stu.get('student_name') or '').strip().upper()
    if (not st_sts or st_sts not in sts_set_numbers) and (not st_name or st_name not in sts_set_names):
        sb_missing_in_sts.append(stu)

print(f"\nSupabase DB students NOT in STS Master list: {len(sb_missing_in_sts)}")
if sb_missing_in_sts:
    print("Sample extra students in DB (first 10):")
    for st in sb_missing_in_sts[:10]:
        st_sts = st.get('student_sts') or st.get('sts_no') or ''
        st_name = st.get('name_english') or st.get('student_name') or ''
        st_class = st.get('enroll_class') or ''
        print(f"  Class: {st_class:4} | STS: {st_sts:10} | Name: {st_name}")

# Class-wise distribution in STS vs Supabase
from collections import Counter
sts_classes = Counter(s['class'] for s in sts_students)
sb_classes = Counter(normalize_class(stu.get('enroll_class')) for stu in supabase_data)

print("\n--- Class-wise counts (STS Master vs Supabase DB) ---")
all_classes = sorted(list(set(list(sts_classes.keys()) + list(sb_classes.keys()))), key=lambda x: (int(x) if x.isdigit() else 99, x))
for c in all_classes:
    print(f"Class {c:4}: STS = {sts_classes.get(c, 0):3} | DB = {sb_classes.get(c, 0):3}")

# Also check gender breakdown in STS Master List
sts_gender_class = {}
for s in sts_students:
    c = s['class']
    g = s['gender']
    if c not in sts_gender_class:
        sts_gender_class[c] = {'Boy': 0, 'Girl': 0, 'Total': 0}
    if g == 'Boy':
        sts_gender_class[c]['Boy'] += 1
    elif g == 'Girl':
        sts_gender_class[c]['Girl'] += 1
    sts_gender_class[c]['Total'] += 1

print("\n--- STS Master List Class & Gender Table ---")
for c in sorted(sts_gender_class.keys(), key=lambda x: (int(x) if x.isdigit() else 99, x)):
    stats = sts_gender_class[c]
    print(f"Class {c:4}: Boys = {stats['Boy']:3} | Girls = {stats['Girl']:3} | Total = {stats['Total']:3}")
