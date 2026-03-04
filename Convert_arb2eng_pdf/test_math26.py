import re
from deep_translator import GoogleTranslator

# Okay, so the output PDF clearly contains "Large = Small - 1".
# The input text that generated this in the Arabic PDF MUST be "= الكبير - الصغير - 1"
# The question is how to fix this exact string in Python.
# If I have a string `t` coming back from translation as "Large = Small - 1"...
# Let's say it didn't even go through `fix_math` properly because it lacked '=', or maybe it did go through `fix_math` and the final output was "Large = Small - 1".

# Let's test `fix_math()` on "Large = Small - 1" directly.

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')
        
        # Google translates isolated "= الكبير - الصغير - 1" into "Large = Small - 1"
        t_new = re.sub(r'(?i)Large\s*=\s*Small', '= Large - Small', t_new)
        
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            reversed_t = " ".join(tokens)
            
            reversed_t = re.sub(r'(?i)Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'(?i)Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'(?i)Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'(?i)Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            reversed_t = re.sub(r'(?i)Small\s*-\s*Large', 'Large - Small', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(f"Result for 'Large = Small - 1':     {fix_math('Large = Small - 1')}")
print(f"Result for 'large = small - 1':     {fix_math('large = small - 1')}")
print(f"Result for '= big - small - 1':     {fix_math('= big - small - 1')}")
