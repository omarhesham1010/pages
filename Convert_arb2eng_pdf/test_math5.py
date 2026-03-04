import re

texts = [
    "= كبير - صغير + 1",
    "١ + صغير - كبير =",
    "= الكبير - الصغير + 1"
]

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('كبير', 'large').replace('big', 'large').replace('major', 'large')
        t_new = t_new.replace('الصغير', 'small').replace('الأصغر', 'small').replace('صغير', 'small').replace('minor', 'small')
        
        tokens = [tok for tok in re.split(r'(\s+|[=+\-*/])', t_new) if tok.strip() or tok in '=+-*/']
        # tokens.reverse() reversed tokens doesn't seem to make `= كبير - صغير + 1` into `= large - small + 1`
        # Because the PDF might extract it as "1 + صغير - كبير =" ? 
        print("Raw Tokens:", tokens)
        
        # If the user says "= كبير - صغير + 1" should be "= large - small + 1", then the word order is exactly the same!
        # Which means we don't need to reverse it if Google already keeps the order, OR if we just want a unified format?
        tokens.reverse()
        rev = "".join(tokens)
        
        non_rev = "".join(tokens[::-1]) # original order
        
        return f"Reversed: {rev} | Not reversed: {non_rev}"
    return t

for text in texts:
    print(f"Original: {text}")
    res = fix_math(text)
    print(f"Result:\n{res}")
    print("---")
