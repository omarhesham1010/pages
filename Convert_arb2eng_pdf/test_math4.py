import re

texts = [
    "الكبير - الصغير + 1",
    "الصغير + 1 = الكبير",
    "= الكبير - الصغير + 1",
    "1 + minor = major"
]

def fix_math(t):
    # First, handle specific math phrases with minor/major / large/small
    # The Arabic keywords might have been translated to English or left as is
    t_lower = t.lower()
    
    # If the text has major/minor/large/small/big AND an equal sign or math operators
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        # Standardize Arabic to English terms before reversing
        t = t.replace('الكبير', 'large').replace('الأكبر', 'large').replace('big', 'large').replace('major', 'large')
        t = t.replace('الصغير', 'small').replace('الأصغر', 'small').replace('minor', 'small')
        
        # Now we tokenize and reverse
        # e.g., "1 + small = large"  -> "large = small + 1"
        # Since it's LTR reading an RTL string extracted backwards
        tokens = [tok for tok in re.split(r'(\s+|[=+\-*/])', t) if tok.strip() or tok in '=+-*/']
        tokens.reverse()
        return "".join(tokens)
        
    # Standard fix_math check
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
        
    return t

for text in texts:
    print(f"Original: {text}")
    res = fix_math(text)
    print(f"Result: {res}")
    print("---")

