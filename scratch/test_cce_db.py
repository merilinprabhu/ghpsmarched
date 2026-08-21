import urllib.request, json

SUPABASE_URL = "https://gsayvnnnfrrkwdfwocbu.supabase.co"
SUPABASE_KEY = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS"

# Test 1: plain query
url1 = f"{SUPABASE_URL}/rest/v1/admissions?select=school_id&limit=10"
req1 = urllib.request.Request(url1, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})

with urllib.request.urlopen(req1) as resp:
    data1 = json.loads(resp.read().decode('utf-8'))
    print("Sample school_ids in admissions:", data1)

# Test 2: cce_evaluations query
url2 = f"{SUPABASE_URL}/rest/v1/cce_evaluations?select=student_id,marks&exam_type=eq.FA1&limit=5"
req2 = urllib.request.Request(url2, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})

try:
    with urllib.request.urlopen(req2) as resp:
        data2 = json.loads(resp.read().decode('utf-8'))
        print("cce_evaluations query returned:", len(data2), "records")
except Exception as e:
    print("cce_evaluations query error:", e)
