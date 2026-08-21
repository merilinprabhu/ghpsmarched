import urllib.request, json, csv, io, re, sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['SatsCompare.html', 'StsCompare.html', 'dashboard.html', 'StudentList.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        txt = f.read()
    urls = re.findall(r'https://docs\.google\.com/spreadsheets/[^\s\'\"\`]+', txt)
    print(f'{fn}:', set(urls))
