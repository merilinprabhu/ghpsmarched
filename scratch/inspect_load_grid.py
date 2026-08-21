with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('async function checkAndLoadGrid')
print(text[idx:idx+4000])
