import urllib.request, json

SUPABASE_URL = "https://gsayvnnnfrrkwdfwocbu.supabase.co"
SUPABASE_KEY = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS"

url = f"{SUPABASE_URL}/rest/v1/admissions?select=id,student_name,name_english,father_name_kn,father_name_az,mother_name_kn,mother_name_az,app_no,student_sts,enroll_class,gender,caste,status&is_admitted=neq.false"
req = urllib.request.Request(url, headers={
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

def normalize_class(class_str):
    if not class_str: return ""
    clean = str(class_str).strip().lower()
    if "lkg" in clean or "kg1" in clean: return "LKG"
    if "ukg" in clean or "kg2" in clean: return "UKG"
    for num in range(1, 11):
        if clean == str(num) or clean == f"class {num}" or clean == f"{num}th" or clean == f"{num}st" or clean == f"{num}nd" or clean == f"{num}rd":
            return str(num)
    return str(class_str).strip()

cls7_students = [s for s in data if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED'] and normalize_class(s.get('enroll_class')) == '7']

print(f"Total Class 7 active students loaded: {len(cls7_students)}")
for i, s in enumerate(cls7_students[:5]):
    print(f"  {i+1}. {s.get('name_english')} ({s.get('student_name')}) - STS: {s.get('app_no')}")
