import fitz

doc = fitz.open("/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf")

for page_num, page in enumerate(doc):
    text_dict = page.get_text("dict")
    for block in text_dict["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                txt = span["text"].strip()
                if "الكبير" in txt or "الصغير" in txt or "كبير" in txt or "صغير" in txt:
                    print(f"RAW PDF TEXT: '{txt}'")
                    print("---")
