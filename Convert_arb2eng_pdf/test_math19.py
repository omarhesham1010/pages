import fitz
import re
from deep_translator import GoogleTranslator

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

def test_on_all():
    count = 0
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0: continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text: continue
                    if "الكبير" in text or "الصغير" in text or "كبير" in text or "صغير" in text:
                        if "=" in text:
                            print(f"> RAW: '{text}'")
                            trans = translator.translate(text)
                            print(f"> GOOGLE: '{trans}'")
                            fixed = fix_math(trans)
                            print(f"> FIXED: '{fixed}'")
                            print("--------------------")

test_on_all()
