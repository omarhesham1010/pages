import re

text1 = "14 = 1 - 35 50 - = 1 - Small - Large" # Google translated
text2 = "Large = - Small - 1 = 99 - 3 - 1 = 95" 
text3 = "1 + small = large"
text4 = "large - small - 1 = 50 - 35 - 1 = 14" # The user said it was written "Small - Large - 1 = 50 - 35 - 1 = 14"

def fix_math(t):
    t_lower = t.lower()
    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
    has_math_word = any(w in t_lower for w in math_words)
    has_math_symbol = any(c in t for c in '=+-*/')
    
    if has_math_word and has_math_symbol:
        t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
        t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')

        t_new = t_new.replace('–', '-')

        tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
        
        # When does it actually need reversing?
        # PyMuPDF extracts equations backward.
        # "الكبير - الصغير - 1 = 14" becomes "14 = 1 - الصغير - الكبير"
        # Since "Large" and "Small" are in tokens, we can actually just sort the logic out.
        # If "Large" appears *after* "Small" in the raw backward extraction: `... Small - Large`
        # Then reversing it makes it `Large - Small ...` which is correct.
        
        # If the Arabic text is "= الكبير - الصغير" -> backward extraction is "الصغير - الكبير =" -> "Small - Large ="
        # Reversing makes it "= Large - Small", correct.
        
        # What if the user said it rendered as "Small - Large - 1 = 50 - 35 - 1 = 14"?
        # That means it was NOT reversed! Or it was reversed improperly.
        # Let's see: if extraction is "14 = 1 - 35 - 50 = 1 - Small - Large"
        # Since it does NOT start with '=', my old logic REVERSED it to:
        # "Large - Small - 1 = 50 - 35 - 1 = 14".
        # But wait! If it reversed to "Large - Small", why did user complain it was "Small - Large"?
        # Ah. User said: 
        # الكبير – الصغير - 1 = – 50 35 - 1 = 14
        # مكتوبه Small - Large - 1 = 50 - 35 - 1 = 14
        # If it was WRITTEN (outputted) as Small - Large, it means it started with `Large` and got outputted backwards to `Small`?
        pass

