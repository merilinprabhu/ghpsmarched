import urllib.request, json

SUPABASE_URL = "https://gsayvnnnfrrkwdfwocbu.supabase.co"
SUPABASE_KEY = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS"

# Test query with school_id.eq.GHPS_MARCHED
url = f"{SUPABASE_URL}/rest/v1/admissions?select=id&or=(school_id.eq.GHPS_MARCHED,school_id.is.null)"
req = urllib.request.Request(url, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("Success:", len(data))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
