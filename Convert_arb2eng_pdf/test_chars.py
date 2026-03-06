import fitz
doc = fitz.open("book_0.pdf")
page = doc[0]
text_instances = []

text_dict = page.get_text("dict")
for block in text_dict["blocks"]:
    if block["type"] != 0: continue
    for line in block["lines"]:
        for span in line["spans"]:
            txt = span["text"].strip()
            # print all 1-character strings
            if len(txt) == 1:
                print(f"Char: '{txt}' at {fitz.Rect(span['bbox'])}")
            if "Legend" in txt or "training" in txt.lower():
                print(f"Word: '{txt}' at {fitz.Rect(span['bbox'])}")
