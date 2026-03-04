import re

text = "= الكبير - الصغير - 1"

import fitz
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='ar', target='en')
google_output = translator.translate(text)
print(f"Google translated: {google_output}")

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # Determine if we should reverse based on the position of the equals sign or layout
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            reversed_t = " ".join(tokens)
            
            # Google translates the messy extraction as "95 = 1 - 3 - 99 = 1 - Minor - = Major"
            reversed_t = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
            reversed_t = re.sub(r'Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
            reversed_t = re.sub(r'Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
            
            # "Large = Small - 1" ? Let's see if google outputs that
            reversed_t = re.sub(r'Small\s*-\s*Large', 'Large - Small', reversed_t)
            
            return reversed_t
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

print(f"Result logic: {fix_math(google_output)}")

