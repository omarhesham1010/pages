import re

texts = [
    "= كبير - صغير - 1 = 99 - 3 - 1 = 95",
    "95 = 1 - 3 - 99 = 1 - صغير - كبير =",
    "1 + minor = major"
]

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    # Process replacements
    t_new = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('big', 'large').replace('major', 'large').replace('كبير', 'large')
    t_new = t_new.replace('الصغير', 'small').replace('الأصغر', 'small').replace('minor', 'small').replace('صغير', 'small')
        
    print(f"DEBUG After replaces: {t_new}")
        
    if has_math_word and has_math_symbol:
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # Determine reverse direction
        # If the Arabic original was `= الكبير - الصغير - 1 = 99 - ... `
        # What is the PyMuPDF exact extracted text? Note that RTL math gets extracted fully backwards sometimes.
        # Example: the user says the result currently is: Major = - Minor - 1 = 99 - 3 - 1 = 95
        # My script produced: large = - small - 1 = 99 - 3 - 1 = 95 ?
        
        # Let's see what PyMuPDF normally extracts for that string: "95 = 1 - 3 - 99 = 1 - صغير - كبير ="
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            return " ".join(tokens)
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

for text in texts:
    print(f"Original: {text}")
    res = fix_math(text)
    print(f"Result:\n{res}")
    print("---")
