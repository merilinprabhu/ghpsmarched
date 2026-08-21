with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// Fallback to local students')
print(text[idx:idx+4000])
