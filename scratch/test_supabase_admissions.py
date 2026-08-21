import urllib.request, json

SUPABASE_URL = "https://gsayvnnnfrrkwdfwocbu.supabase.co"
SUPABASE_KEY = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS"

url = f"{SUPABASE_URL}/rest/v1/admissions?select=id,student_name,name_english,father_name_kn,father_name_az,mother_name_kn,mother_name_az,app_no,student_sts,enroll_class,gender,caste,status&is_admitted=neq.false"
req = urllib.request.Request(url, headers={
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print(f"Total active admissions returned: {len(data)}")
        c7 = [s for s in data if s.get('enroll_class') in ['7', 'Class 7', '7ನೇ']]
        print(f"Class 7 count: {len(c7)}")
except Exception as e:
    print(f"Error fetching from Supabase: {e}")
