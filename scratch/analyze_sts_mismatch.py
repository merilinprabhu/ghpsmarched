import urllib.request, json, csv, io, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch STS Google Sheet (520 students)
sheet_url = 'https://docs.google.com/spreadsheets/d/14_T-s2rGf2Gvdfg9dG-Ym0hN1v-w0pB3tK76U7n9T10/export?format=csv'
with open('SatsCompare.html', 'r', encoding='utf-8') as f:
    txt = f.read()

m = re.search(r"DEFAULT_SPREADSHEET_URL\s*=\s*['\"]([^'\"]+)['\"]", txt)
if m:
    sheet_url = m.group(1)

print('Using Sheet URL:', sheet_url)
req_sheet = urllib.request.Request(sheet_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_sheet) as resp:
    sheet_content = resp.read().decode('utf-8', errors='ignore')

reader = csv.reader(io.StringIO(sheet_content))
header = next(reader)
sheet_rows = list(reader)
print(f'Total rows in STS Sheet: {len(sheet_rows)}')

# Let's inspect STS header columns
print('STS Header:', header[:10])

# Parse STS students
sts_students = []
for idx, r in enumerate(sheet_rows, 1):
    sts_no = r[1].strip() if len(r) > 1 else ''
    name = r[2].strip() if len(r) > 2 else ''
    father = r[3].strip() if len(r) > 3 else ''
    cls = r[4].strip() if len(r) > 4 else ''
    gender = r[5].strip() if len(r) > 5 else ''
    dob = r[6].strip() if len(r) > 6 else ''
    caste = r[7].strip() if len(r) > 7 else ''
    sts_students.append({
        'idx': idx,
        'sts': sts_no,
        'name': name,
        'father': father,
        'class': cls,
        'gender': gender,
        'dob': dob,
        'caste': caste
    })

# Count STS by Class
sts_by_class = {}
for s in sts_students:
    cls = s['class']
    sts_by_class[cls] = sts_by_class.get(cls, 0) + 1
print('\n--- STS Sheet Student Counts by Class (Total: 520) ---')
for c, cnt in sorted(sts_by_class.items()):
    print(f'  Class {c:4}: {cnt:3} students')

# 2. Fetch Supabase admissions table
url = 'https://gsayvnnnfrrkwdfwocbu.supabase.co/rest/v1/admissions?select=*'
headers = {
    'apikey': 'sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS',
    'Authorization': 'Bearer sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS'
}
req_db = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req_db) as resp:
    db_students = json.loads(resp.read().decode('utf-8'))

print(f'\nTotal rows in Supabase admissions table: {len(db_students)}')

# Analyze statuses in DB
status_counts = {}
for s in db_students:
    st = s.get('status') or 'ACTIVE'
    status_counts[st] = status_counts.get(st, 0) + 1
print('DB by Status:', status_counts)

# Active students in DB
active_db = [s for s in db_students if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED']]
print(f'Active DB Students: {len(active_db)}')

# Count DB by Class
db_by_class = {}
for s in active_db:
    cls = str(s.get('enroll_class') or 'Unassigned').strip()
    db_by_class[cls] = db_by_class.get(cls, 0) + 1
print('\n--- DB Active Student Counts by Class (Total: ' + str(len(active_db)) + ') ---')
for c, cnt in sorted(db_by_class.items()):
    print(f'  Class {c:4}: {cnt:3} students')

# 3. Detailed Cross Matching: Match each STS student with DB active student
clean_sts_map = {}
for s in active_db:
    sts_val = str(s.get('student_sts') or s.get('sts_no') or s.get('app_no') or s.get('enrolment_no') or '').replace(' ', '').strip()
    if sts_val and len(sts_val) >= 6:
        clean_sts_map[sts_val] = s

matched_sts = []
missing_sts_in_db = []

for s in sts_students:
    clean_s = s['sts'].replace(' ', '').strip()
    matched = None
    if clean_s in clean_sts_map:
        matched = clean_sts_map[clean_s]
    else:
        # Try matching by normalized name and class
        s_name = re.sub(r'[^a-zA-Z0-9]', '', s['name'].lower())
        for d in active_db:
            d_name = re.sub(r'[^a-zA-Z0-9]', '', (d.get('name_english') or d.get('student_name') or '').lower())
            d_cls = str(d.get('enroll_class') or '').strip()
            if s_name and d_name and (s_name == d_name) and (str(s['class']) == d_cls):
                matched = d
                break
    
    if matched:
        matched_sts.append((s, matched))
    else:
        missing_sts_in_db.append(s)

print(f'\n--- Matching Summary ---')
print(f'Matched STS students in DB: {len(matched_sts)} / 520')
print(f'Missing STS students in DB: {len(missing_sts_in_db)}')
for m in missing_sts_in_db:
    print(f"  STS: {m['sts']:12} | Name: {m['name']:25} | Father: {m['father']:20} | Class: {m['class']:3} | DOB: {m['dob']}")

# 4. Check extra students in DB that are NOT in STS Master list
matched_db_ids = set(m[1].get('id') for m in matched_sts)
extra_db_students = [s for s in active_db if s.get('id') not in matched_db_ids]
print(f'\nExtra Active DB Students not in STS Master List: {len(extra_db_students)}')
for e in extra_db_students[:20]:
    app = e.get('app_no') or '-'
    sts = e.get('student_sts') or e.get('sts_no') or '-'
    name = e.get('name_english') or e.get('student_name') or '-'
    cls = e.get('enroll_class') or '-'
    dob = e.get('dob') or '-'
    print(f"  ID: {e.get('id')[:8]} | App: {app:8} | STS: {sts:12} | Name: {name:20} | Class: {cls:3} | DOB: {dob}")
