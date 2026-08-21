with open('CceAssessmet.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Exception loading CCE evaluations')
print(text[idx:idx+2500].encode('ascii', errors='replace').decode('ascii'))
