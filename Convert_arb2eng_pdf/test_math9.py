import re

text1 = "Major = - Minor - 1 = 99 - 3 - 1 = 95"
text2 = "large = - small - 1 = 99 - 3 - 1 = 95"
text3 = "1 + minor = major"
text4 = "= الكبير - الصغير - 1 = 99 - 3 - 1 = 95"

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('big', 'large').replace('major', 'large').replace('Major', 'large').replace('كبير', 'large')
        t_new = t_new.replace('الصغير', 'small').replace('الأصغر', 'small').replace('minor', 'small').replace('Minor', 'small').replace('صغير', 'small')
        
        # Sometimes google translates "= الكبير - الصغير" as "Major = - Minor" which breaks the equation.
        # We can fix this specific artifact by Regex replacing:
        t_new = re.sub(r'large\s*=\s*-\s*small', '= large - small', t_new)
        t_new = re.sub(r'small\s*=\s*-\s*large', '= small - large', t_new)
        
        # Cleanly split by operators, retaining them, and stripping whitespace
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            return " ".join(tokens)
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t


for t in [text1, text2, text3, text4]:
    print(f"Original: {t}")
    print(f"Result: {fix_math(t)}")
    print("---")
