from deep_translator import GoogleTranslator

def arabic_to_english(text):
    translated = GoogleTranslator(source='ar', target='en').translate(text)
    return translated


# مثال
arabic_text = "عدد الطلاب بين ٣ و ٩٩ هو ٩٥"
english_text = arabic_to_english(arabic_text)

print(english_text)