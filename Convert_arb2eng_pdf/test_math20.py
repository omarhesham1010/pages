import fitz
from deep_translator import GoogleTranslator
import re

doc = fitz.open("book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')

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

count = 0
for page in doc:
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0: continue
        for line in block["lines"]:
            line_text = ""
            for span in line["spans"]:
                line_text += span["text"]
            
            # This is how full_convert.py formats the string:
            original_text = line_text.strip()
            
            if "الكبير" in original_text or "الصغير" in original_text:
                if "=" in original_text:
                    print(f"RAW: '{original_text}'")
                    try:
                        trans = translator.translate(original_text)
                        print(f"GOOGLE: '{trans}'")
                        fixed = fix_math(trans)
                        print(f"FIXED: '{fixed}'")
                    except Exception as e:
                        pass
                    print("---")
            
