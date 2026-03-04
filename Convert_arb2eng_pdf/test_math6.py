import re

texts = [
    "= كبير - صغير + 1",
    "١ + صغير - كبير =",
    "= الكبير - الصغير + 1",
    "1 + minor = major"
]

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('big', 'large').replace('major', 'large').replace('كبير', 'large')
        t_new = t_new.replace('الصغير', 'small').replace('الأصغر', 'small').replace('minor', 'small').replace('صغير', 'small')
        
        # When splitting with regex capturing groups, we capture spaces as well
        # Let's clean the extra whitespace so we can have predictable formatting
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # Determine if we should reverse based on the position of the equals sign or layout
        # Let's say we ALWAYS want the layout `variable = formula` or `= formula`.
        # When Arabic equation specifies `= كبير - صغير + 1`, we want it to output `= large - small + 1` with spaces.
        
        if t_new.strip().startswith('='):
            # Do not reverse, just add normal spaces
            return " ".join(tokens)
        else:
            # Reverse tokens
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
