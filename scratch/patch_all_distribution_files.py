import re, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. TextbookDistribution.html
with open('TextbookDistribution.html', 'r', encoding='utf-8') as f:
    txt = f.read()

target = """        admissionsList = (students || [])
          .filter(s => {
            const isAdm = s.is_admitted === undefined || s.is_admitted === null ? true : s.is_admitted;
            return isAdm === true || isAdm === 'true';
          })"""

replacement = """        const localTrashed = JSON.parse(localStorage.getItem('trashed_students_list') || '[]');
        const trashedKeys = new Set(localTrashed.map(t => String(t.id || t.app_no || t.student_sts || '').replace(/\\s+/g, '').toLowerCase()));

        admissionsList = (students || [])
          .filter(s => {
            const isNotOut = s.status !== 'TC_OUT' && s.status !== 'DELETED' && s.status !== 'REMOVED';
            const sKey1 = String(s.id || '').replace(/\\s+/g, '').toLowerCase();
            const sKey2 = String(s.student_sts || s.app_no || '').replace(/\\s+/g, '').toLowerCase();
            const isNotTrashed = (!sKey1 || !trashedKeys.has(sKey1)) && (!sKey2 || !trashedKeys.has(sKey2));
            const isAdm = s.is_admitted === undefined || s.is_admitted === null ? true : s.is_admitted;
            return isNotOut && isNotTrashed && (isAdm === true || isAdm === 'true');
          })"""

if target in txt:
    txt = txt.replace(target, replacement)
    with open('TextbookDistribution.html', 'w', encoding='utf-8') as f:
        f.write(txt)
    print("Patched TextbookDistribution.html")

# 2. UniformDistribution.html
with open('UniformDistribution.html', 'r', encoding='utf-8') as f:
    txt2 = f.read()

target2 = """        admissionsList = (students || [])
          .filter(s => {
            const isAdm = s.is_admitted === undefined || s.is_admitted === null ? true : s.is_admitted;
            return isAdm === true || isAdm === 'true';
          })"""

if target2 in txt2:
    txt2 = txt2.replace(target2, replacement)
    with open('UniformDistribution.html', 'w', encoding='utf-8') as f:
        f.write(txt2)
    print("Patched UniformDistribution.html")

# 3. ShoeSocksDistribution.html
with open('ShoeSocksDistribution.html', 'r', encoding='utf-8') as f:
    txt3 = f.read()

if target2 in txt3:
    txt3 = txt3.replace(target2, replacement)
    with open('ShoeSocksDistribution.html', 'w', encoding='utf-8') as f:
        f.write(txt3)
    print("Patched ShoeSocksDistribution.html")

# 4. HeightWeightTracker.html
with open('HeightWeightTracker.html', 'r', encoding='utf-8') as f:
    txt4 = f.read()

if target2 in txt4:
    txt4 = txt4.replace(target2, replacement)
    with open('HeightWeightTracker.html', 'w', encoding='utf-8') as f:
        f.write(txt4)
    print("Patched HeightWeightTracker.html")

# 5. EggBananaDistribution.html
with open('EggBananaDistribution.html', 'r', encoding='utf-8') as f:
    txt5 = f.read()

if target2 in txt5:
    txt5 = txt5.replace(target2, replacement)
    with open('EggBananaDistribution.html', 'w', encoding='utf-8') as f:
        f.write(txt5)
    print("Patched EggBananaDistribution.html")
