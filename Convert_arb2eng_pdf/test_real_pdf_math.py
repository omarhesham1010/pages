import fitz
import re
from deep_translator import GoogleTranslator

doc = fitz.open("/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')
        
        t_new = re.sub(r'Large\s*=\s*-\s*Small', '= Large - Small', t_new)
        t_new = re.sub(r'Small\s*=\s*-\s*Large', '= Small - Large', t_new)
        
        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        if t_new.strip().startswith('='):
            return " ".join(tokens)
        else:
            tokens.reverse()
            return " ".join(tokens)
            
    if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
        return " ".join(reversed(t.split()))
    return t

for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if "99" in span["text"] or "95" in span["text"] or "الكبير" in span["text"] or "صغير" in span["text"] or "كبير" in span["text"] or "الصغير" in span["text"]:
                    text = span["text"].strip()
                    if "=" in text and "-" in text:
                        print(f"--- MATCH PAGE {page_num} ---")
                        print(f"RAW PDF EXTRACT: {repr(text)}")
                        
                        try:
                            translated_direct = translator.translate(text)
                            print(f"Google Translated Direct: {repr(translated_direct)}")
                            
                            fixed = fix_math(translated_direct)
                            print(f"After fix_math(Google_output): {repr(fixed)}")
                        except Exception as e:
                            print(f"Translation failed: {e}")
