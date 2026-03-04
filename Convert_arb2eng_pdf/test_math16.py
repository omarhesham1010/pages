import re

text = "Large = Small - 1" # Google translated "= الكبير - الصغير - 1" to this somehow (or PyMuPDF extracted it).

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        # Since Google completely ruined "= الكبير - الصغير - 1" into "Large = Small - 1" FOR THE USER:
        # We need to catch this exact pattern of error.
        # If it exactly matches "Large = Small" or "Large = + Small", we fix it.
        # Note: "Small = Large" -> "= Small + Large" ? No, Arabic is usually "= Large - Small".
        
        t_new = re.sub(r'Large\s*=\s*Small', '= Large - Small', t_new)
        
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            reversed_t = " ".join(tokens)
            
            reversed_t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            # Since my logic above replaces `Large = Small` into `= Large - Small`,
            # Let's ensure if it was right-to-left reversed later, it doesn't break.
            
            reversed_t = re.sub(r'Small\s*-\s*Large', 'Large - Small', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(f"Result logic: {fix_math(text)}")

