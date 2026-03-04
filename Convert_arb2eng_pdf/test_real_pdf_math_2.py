import re

text = "95 = 1 - 3 - 99 = 1 - Minor - = Major"

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        # Google translates the messy extraction as "95 = 1 - 3 - 99 = 1 - Minor - = Major"
        # Since it's completely backward, if we reverse it raw: "Major = - Minor - 1 = 99 - 3 - 1 = 95"
        # We need to change "Major = - Minor" -> "= Major - Minor".
        # Which is exactly what we were trying, but we wrote: `= Large - Small`
        
        # New robust logic:
        # Instead of replacing on t_new, let's reverse first (since PyMuPDF extracted it backward)
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # If it starts with equals after reversal, it's correct Arabic reading style
        if t_new.strip().startswith('='):
            # Already left-to-right correctly? Unlikely based on PyMuPDF tests, but we kept it.
            return " ".join(tokens)
        else:
            tokens.reverse()
            reversed_t = " ".join(tokens)
            
            # Now we have "Large = - Small - 1 = 99 - 3 - 1 = 95"
            # It should be "= Large - Small - 1 = ... "
            # Fix the leading equals:
            # Match "Large = - Small" -> "= Large - Small"
            # Or "Large = + Small" -> "= Large + Small"
            reversed_t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(f"Original: {text}")
print(f"Fixed:\n{fix_math(text)}")
