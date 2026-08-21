import urllib.request, json, csv, io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Helper functions
def normalize_class(val):
    if not val: return ''
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

# 1. Fetch Supabase admissions
url = 'https://gsayvnnnfrrkwdfwocbu.supabase.co/rest/v1/admissions?select=*'
headers = {
    'apikey': 'sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS',
    'Authorization': 'Bearer sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    supabase_data = json.loads(resp.read().decode('utf-8'))

# 2. Fetch Google Sheet STS CSV (520 students)
sheet_url = 'https://docs.google.com/spreadsheets/d/1awYBM024orzUascz9uTYIeXg6rN55sbSJj7hIrhMWp8/gviz/tq?tqx=out:csv&gid=1852377268'
req_sheet = urllib.request.Request(sheet_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_sheet) as resp:
    sheet_csv_text = resp.read().decode('utf-8')

reader = csv.reader(io.StringIO(sheet_csv_text))
sheet_rows = list(reader)
header = sheet_rows[0]
data_rows = sheet_rows[1:]

print(f"Total Google Sheet STS Rows: {len(data_rows)}")
print(f"Total Supabase DB records: {len(supabase_data)}")

# Analyze DB Statuses
status_map = {}
for s in supabase_data:
    st = s.get('status') or 'ACTIVE'
    status_map[st] = status_map.get(st, 0) + 1
print(f"Supabase DB Status breakdown: {status_map}")

active_db = [s for s in supabase_data if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED']]
print(f"Active DB students (shown in StudentList): {len(active_db)}")

# Let's see STS classwise breakdown vs DB classwise breakdown
sts_parsed = []
for r in data_rows:
    sts_parsed.append({
        'sts': clean_sts(r[1]),
        'name': r[2].strip(),
        'father': r[3].strip(),
        'class': normalize_class(r[4]),
        'gender': r[5].strip(),
        'dob': r[6].strip(),
        'caste': r[7].strip()
    })

sts_class_counts = {}
for s in sts_parsed:
    c = s['class']
    sts_class_counts[c] = sts_class_counts.get(c, 0) + 1

db_class_counts = {}
for s in active_db:
    c = normalize_class(s.get('enroll_class') or s.get('className') or '')
    db_class_counts[c] = db_class_counts.get(c, 0) + 1

print("\n================ CLASSWISE COMPARISON: STS SHEET (520) vs DB ACTIVE (518) ================")
print(f"{'Class':<10} | {'STS Sheet (Master)':<20} | {'Site DB Active (Now)':<20} | {'Difference':<15}")
print("-" * 75)
all_classes = ['LKG', 'UKG', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
for c in all_classes:
    s_cnt = sts_class_counts.get(c, 0)
    d_cnt = db_class_counts.get(c, 0)
    diff = d_cnt - s_cnt
    diff_str = f"+{diff}" if diff > 0 else (str(diff) if diff < 0 else "0 (Match)")
    print(f"Class {c:<4} | {s_cnt:<20} | {d_cnt:<20} | {diff_str:<15}")

print("-" * 75)
print(f"{'TOTAL':<10} | {sum(sts_class_counts.values()):<20} | {sum(db_class_counts.values()):<20} | {sum(db_class_counts.values()) - sum(sts_class_counts.values()):<15}")

# Find which STS students are missing or having wrong class/STS in DB
print("\n================ CHECKING 520 STS STUDENTS IN DB ================")
sts_in_db = 0
sts_not_in_db = []

# Build fast lookup map for active DB
db_by_sts = {}
for s in active_db:
    s_sts = clean_sts(s.get('student_sts') or s.get('sts_no') or s.get('app_no') or s.get('enrolment_no') or '')
    if s_sts:
        db_by_sts[s_sts] = s

for s in sts_parsed:
    s_clean = s['sts']
    if s_clean in db_by_sts:
        sts_in_db += 1
    else:
        # Check name fuzzy
        s_name = re.sub(r'[^A-Z0-9]', '', s['name'].upper())
        found = False
        for d in active_db:
            d_name = re.sub(r'[^A-Z0-9]', '', (d.get('name_english') or d.get('student_name') or '').upper())
            if s_name and d_name and (s_name == d_name or s_name in d_name or d_name in s_name):
                found = True
                break
        if not found:
            sts_not_in_db.append(s)

print(f"Exact STS matched in DB: {sts_in_db} / 520")
print(f"STS students NOT in DB: {len(sts_not_in_db)}")
for m in sts_not_in_db:
    print(f"  Missing: STS {m['sts']} | {m['name']} | Class {m['class']} | Father: {m['father']}")

# Check why Dashboard KPD table was showing different numbers in 1st image
print("\n================ ANALYZING DASHBOARD KPD TABLE (IMAGE 1) ================")
# In Image 1:
# LKG: 24, UKG: 14, 1: 25, 2: 4, 3: 23, 4: 24, 5: 4, 6: 10, 7: 45, 8: 52, 9: 3, 10: 3
# Total: 227 !
# Why were only 227 students showing in dashboard.html in image 1?
# Let's check academic_year or is_admitted in DB!
print("DB Active students by academic_year:")
year_map = {}
for s in active_db:
    yr = str(s.get('academic_year') or 'None')
    year_map[yr] = year_map.get(yr, 0) + 1
print(year_map)

print("DB Active students by is_admitted:")
admit_map = {}
for s in active_db:
    adm = str(s.get('is_admitted'))
    admit_map[adm] = admit_map.get(adm, 0) + 1
print(admit_map)

print("DB Active students with academic_year == '2026-27' by class:")
y26_students = [s for s in active_db if s.get('academic_year') == '2026-27']
y26_class = {}
for s in y26_students:
    c = normalize_class(s.get('enroll_class') or s.get('className') or '')
    y26_class[c] = y26_class.get(c, 0) + 1
for c in all_classes:
    print(f"  Class {c:<4}: {y26_class.get(c, 0)} (vs Image 1)")
