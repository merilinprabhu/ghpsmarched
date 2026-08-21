import urllib.request, json, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch Supabase admissions table for Class 10
url = 'https://gsayvnnnfrrkwdfwocbu.supabase.co/rest/v1/admissions?enroll_class=eq.10&select=*'
headers = {
    'apikey': 'sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS',
    'Authorization': 'Bearer sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS'
}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    class10_students = json.loads(resp.read().decode('utf-8'))

active_10 = [s for s in class10_students if s.get('status') not in ['TC_OUT', 'DELETED', 'REMOVED']]
print(f"Total Active Class 10 Students in Supabase admissions table: {len(active_10)}")

print("\n--- Listing the 3 Verified Students in Class 10 ---")
for s in active_10:
    sts = str(s.get('student_sts') or s.get('sts_no') or s.get('app_no'))
    name = str(s.get('name_english') or s.get('student_name'))
    if sts.replace(' ', '') in ['131853739', '126929716', '129459515']:
        print(f"ID: {s.get('id')}")
        print(f"  Name (English): {s.get('name_english')}")
        print(f"  Name (Kannada): {s.get('student_name')}")
        print(f"  STS Number:     {s.get('student_sts')}")
        print(f"  Class:          {s.get('enroll_class')}")
        print(f"  Gender:         {s.get('gender')}")
        print(f"  DOB:            {s.get('dob')}")
        print(f"  Father Name:    {s.get('father_name_az') or s.get('father_name_kn') or s.get('father_name') or '-'}")
        print(f"  School ID:      {s.get('school_id')}")
        print(f"  Status:         {s.get('status')}")
        print(f"  is_admitted:    {s.get('is_admitted')}")
        print("-" * 50)

# Check how other pages query students (e.g. StudentList.html, CCE, LBA)
print("\n--- How other modules query Class 10 ---")
print("1. StudentList.html: SELECT * FROM admissions WHERE status != 'TC_OUT' / 'DELETED' (Filters by Class 10 -> will show all 48)")
print("2. CCE Assessment: SELECT * FROM admissions WHERE enroll_class = '10' (Loads all 48 students in Class 10 dropdown)")
print("3. LBA Assessment: SELECT * FROM admissions WHERE enroll_class = '10' (Loads all 48 students in Class 10 dropdown)")
print("4. Attendance / Shoe Tracker / Certificates: Loads from same admissions database.")
