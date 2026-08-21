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

# 1. Fetch Supabase admissions (all records including TC_OUT / DELETED)
url = 'https://gsayvnnnfrrkwdfwocbu.supabase.co/rest/v1/admissions?select=*'
headers = {
    'apikey': 'sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS',
    'Authorization': 'Bearer sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    supabase_data = json.loads(resp.read().decode('utf-8'))

print(f"Total Supabase admissions records: {len(supabase_data)}")

# 10th standard in Supabase DB
db_10th_all = [s for s in supabase_data if normalize_class(s.get('enroll_class') or s.get('className')) == '10']
db_10th_active = [s for s in db_10th_all if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED']]
db_10th_out = [s for s in db_10th_all if s.get('status') in ['TC_OUT', 'DELETED', 'REMOVED']]

print(f"Total 10th in DB (all statuses): {len(db_10th_all)}")
print(f"Active 10th in DB: {len(db_10th_active)}")
print(f"TC_OUT / DELETED 10th in DB: {len(db_10th_out)}")

# 2. Check if there are other students in DB with Class 0 or 9 or other who might be in 10th
print("\n--- Check all active DB students by class ---")
class_dist = {}
for s in supabase_data:
    if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED']:
        c = normalize_class(s.get('enroll_class') or s.get('className'))
        class_dist[c] = class_dist.get(c, 0) + 1
for c, cnt in sorted(class_dist.items()):
    print(f"  Class {c:4}: {cnt:3} students")

# 3. Print all 10th standard students in DB
print(f"\n--- Active 10th standard students in DB ({len(db_10th_active)}) ---")
for idx, s in enumerate(db_10th_active, 1):
    sts = clean_sts(s.get('student_sts') or s.get('sts_no') or s.get('app_no') or '')
    name = s.get('name_english') or s.get('student_name') or ''
    father = s.get('father_name_az') or s.get('father_name_kn') or s.get('father_name') or ''
    gender = s.get('gender') or ''
    dob = s.get('dob') or ''
    print(f"{idx:2}. STS: {sts:12} | Name: {name:25} | Father: {father:20} | {gender:4} | {dob}")

# 4. Print any TC_OUT / DELETED students in 10th standard in DB
if db_10th_out:
    print(f"\n--- TC_OUT / DELETED in 10th standard ({len(db_10th_out)}) ---")
    for idx, s in enumerate(db_10th_out, 1):
        sts = clean_sts(s.get('student_sts') or s.get('sts_no') or s.get('app_no') or '')
        name = s.get('name_english') or s.get('student_name') or ''
        st = s.get('status')
        print(f"{idx:2}. STS: {sts:12} | Name: {name:25} | Status: {st}")
