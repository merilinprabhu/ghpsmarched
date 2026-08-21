import re, glob

def check_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    scripts = re.findall(r'<script(?:\s+[^>]*)?>([\s\S]*?)</script>', code, re.IGNORECASE) if filename.endswith('.html') else [code]
    
    issues = []
    for s_idx, s in enumerate(scripts):
        # find functions
        for m in re.finditer(r'(async\s+)?function\s+([a-zA-Z0-9_$]+)\s*\([^)]*\)\s*\{', s):
            is_async = bool(m.group(1))
            func_name = m.group(2)
            start_pos = m.start()
            
            brace_count = 0
            in_str = False
            str_char = ''
            in_comment = False
            func_body = ''
            
            # Simple bracket matcher
            i = m.end() - 1
            while i < len(s):
                ch = s[i]
                if not in_str:
                    if ch in ('"', "'", '`'):
                        in_str = True
                        str_char = ch
                    elif ch == '{':
                        brace_count += 1
                    elif ch == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            func_body = s[m.start():i+1]
                            break
                else:
                    if ch == '\\':
                        i += 1
                    elif ch == str_char:
                        in_str = False
                i += 1
            
            if not is_async:
                # Remove inner async functions before checking for await
                cleaned_body = re.sub(r'async\s+function[\s\S]*?\{[\s\S]*?\}', '', func_body)
                cleaned_body = re.sub(r'async\s*\([^)]*\)\s*=>[\s\S]*?\}', '', cleaned_body)
                if 'await ' in cleaned_body:
                    line_no = s[:start_pos].count('\n') + 1
                    issues.append((func_name, line_no))
    return issues

print("=== Checking CceAssessmet.html ===")
for fn, lno in check_file('CceAssessmet.html'):
    print(f"  [ERROR] Function '{fn}' at line {lno} has 'await' but is not declared 'async'!")

print("\n=== Checking all HTML files ===")
for html_file in glob.glob('*.html'):
    issues = check_file(html_file)
    if issues:
        print(f"File: {html_file}")
        for fn, lno in issues:
            print(f"  [ERROR] Function '{fn}' at script line {lno} has 'await' but is not declared 'async'!")
