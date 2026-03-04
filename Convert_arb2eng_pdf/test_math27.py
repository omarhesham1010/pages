import re
from deep_translator import GoogleTranslator

# So why did `large = small - 1` return WITHOUT fixing in `full_convert`?
# In full_convert.py:
# def fix_math(t):
#    # ...
#    math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
#    has_math_word = any(w in t_lower for w in math_words)
#
#    if has_math_word and has_math_symbol: ...
#
# BUT WAIT. In my tests I always passed `math_words`! 
# Look closely at test_math26.py: `math_words = ['major', 'minor', 'large', 'small', 'big', ...`
# Let's check WHAT IS WRITTEN IN the actual full_convert.py line 182:
# math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
# It HAS 'large' and 'small'!

# So why would it fail?
# Ah! "has_math_symbol = any(c in t for c in '=+-*/')". 
# If `t` is "Large = Small - 1", it has '=' and '-'. So has_math_symbol is True.
# So it MUST enter the `if has_math_word and has_math_symbol:` block.

# Wait, if it entered the block, it would have executed this:
# t_new = re.sub(r'(?i)Large\s*=\s*Small', '= Large - Small', t_new)
# And the tokens would reverse because it doesn't start with '=':
# tokens = [1, -, Small, -, Large, =] -> "1 - Small - Large ="
# Wait... if `tokens.reverse()` happened on "Large = Small - 1":
# Tokens: ['Large', '=', 'Small', '-', '1']
# Reversed: ['1', '-', 'Small', '=', 'Large'] -> "1 - Small = Large"

# THEN:
# reversed_t = re.sub(r'(?i)Small\s*=\s*-\s*Large', '= Small - Large', reversed_t) # no match
# reversed_t = re.sub(r'(?i)Small\s*-\s*Large', 'Large - Small', reversed_t) # no match

# Result: "1 - Small = Large" !!
# But the user says the final output is "Large = Small - 1" exactly.

# Why is it not reversing?
# Let's add logging to see exactly why!

