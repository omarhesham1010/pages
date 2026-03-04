import fitz
import re
from deep_translator import GoogleTranslator

doc = fitz.open("/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")
translator = GoogleTranslator(source='ar', target='en')


count = 0
for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                if count > 50: break
                text = span["text"].strip()
                if not text: continue
                count += 1
                print("RAW:", repr(text))
                if "محمد" in text or "40" in text or "50" in text or "٥٠" in text:
                    print("--> MATCH <--")
                    try:
                        translated = translator.translate(text)
                        print("Translated:", repr(translated))
                    except:
                        pass

