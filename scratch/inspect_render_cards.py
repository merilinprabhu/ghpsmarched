with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderCards')
print(text[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
