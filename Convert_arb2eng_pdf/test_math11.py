import re

text = "large = - small - 1 = 99 - 3 - 1 = 95"

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')

    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        # Sometimes Google Translate corrupts "= الكبير - الصغير" into "Major = - Minor" 
        t_new = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', t_new)
        t_new = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', t_new)

        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # Determine if we should reverse based on the position of the equals sign or layout
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            return " ".join(tokens)
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(fix_math(text))
