import re
from deep_translator import GoogleTranslator

# The user's text extracted from PDF might look like:
# "14 = 1 - 35 50 - = 1 - الصغير - الكبير" or similar?
# Let's see what PyMuPDF extracts directly from those numbers.
text_original = "الكبير – الصغير - 1 = – 50 35 - 1 = 14"

translator = GoogleTranslator(source='ar', target='en')

# Try translation on mocked extracted variations
mock_extracts = [
    "14 = 1 - 35 50 - = 1 - الصغير – الكبير",
    "الكبير – الصغير - 1 = – 50 35 - 1 = 14", # If extracted correctly LTR
    "14 = 1 - 35 50 - = 1 - الصغير - الكبير"
]

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        # Also replace en dash (–) with normal hyphen (-) so splits work
        t_new = t_new.replace('–', '-')

        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # See what tokens look like right before we reverse
        print("  Tokens BEFORE reverse check:", tokens)
        
        # We were checking if it starts with '='. 
        # But here, "Large - Small - 1 = ..." DOES NOT start with '='!
        # So "Large - Small - 1 = ..." goes to the `else` block and GETS REVERSED.
        # Reverse of ["Large", "-", "Small"] -> ["Small", "-", "Large"]. 
        # Bingo. This is why it became Small - Large.
        
        if t_new.strip().startswith('='):
            # It's naturally left-to-right (very rare for Arabic PDF extraction of equations)
            return " ".join(tokens)
        else:
            # We reverse it
            tokens.reverse()
            reversed_t = " ".join(tokens)
            print("  Tokens AFTER reverse check:", reversed_t)
            
            reversed_t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

for m in mock_extracts:
    print(f"\n--- Testing Extract: {m}")
    trans = translator.translate(m)
    print(f"Google translated: {trans}")
    fixed = fix_math(trans)
    print(f"Result:\n{fixed}")

