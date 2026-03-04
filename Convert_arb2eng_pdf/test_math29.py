import re
from deep_translator import GoogleTranslator

# If string extracted was exactly: "1 - الصغير - الكبير ="
# We know it outputs "= Large - Small - 1". It works.

# WHAT IF the string extracted was:
# "1 - الصغير - الكبير" (NO EQUALS SIGN AT ALL)
# Or Google translated it as "1 - small - large"?
# But wait, it HAS to have an equals sign, the user said it outputs "Large = Small - 1"

# Let's consider the user's literal input from the PDF again: `= الكبير - الصغير - 1`
# If PyMuPDF extracts it strictly right-to-left as tokens: `1 - الصغير - الكبير =`
# Translation is `1 - small - large =`.
# Reversed it gives `= Large - Small - 1`.

# What if PyMuPDF extracted it as `الصغير - الكبير - 1 =` ???
# Try that:
text3 = "small - large - 1 ="
# Reversed: "= 1 - Large - Small". NOT Large = Small - 1.

# HOW DOES "Large = Small - 1" GET GENERATED FROM "= الكبير - الصغير - 1" ???
# The ONLY WAY is if the PRE-REVERSED string was:
# "1 - Small = Large"

# How would PyMuPDF extract "1 - Small = Large"?
# From Arabic: `الكبير = الصغير - 1` (Large = Small - 1)
# Is it POSSIBLE the user's original pdf actually says "الكبير = الصغير - 1" but they MISREAD IT or EXPECT "= الكبير - الصغير - 1" ???

# Let's test `1 - Small = Large`
text4 = "1 - small = large"
def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')
        
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

print(f"OUTPUT 4: {fix_math(text4)}")
