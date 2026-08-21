import urllib.request, json

SUPABASE_URL = "https://gsayvnnnfrrkwdfwocbu.supabase.co"
SUPABASE_KEY = "sb_publishable_Q92Byh3WyIwhrsJ0YNKO4w_sqx3tHMS"

url = f"{SUPABASE_URL}/rest/v1/?apikey={SUPABASE_KEY}"
req = urllib.request.Request(url, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})

try:
    with urllib.request.urlopen(req) as resp:
        schema = json.loads(resp.read().decode('utf-8'))
        cce_cols = schema.get('definitions', {}).get('cce_evaluations', {}).get('properties', {})
        print("cce_evaluations columns:", list(cce_cols.keys()))
        for k, v in cce_cols.items():
            print(f"  {k}: {v.get('type')} (format: {v.get('format')})")
except Exception as e:
    print("Schema fetch error:", e)
