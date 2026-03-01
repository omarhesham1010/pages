import fitz  # PyMuPDF

# تحويل الأرقام العربية لإنجليزية
def convert_arabic_digits(text):
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    return text.translate(str.maketrans(arabic_digits, english_digits))


def replace_digits_in_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)

    for page in doc:
        text_instances = page.get_text("dict")["blocks"]

        for block in text_instances:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"]
                        new_text = convert_arabic_digits(original_text)

                        if original_text != new_text:
                            rect = fitz.Rect(span["bbox"])

                            # امسح النص القديم
                            page.add_redact_annot(rect, fill=(1, 1, 1))
                            page.apply_redactions()

                            # اكتب الجديد في نفس المكان
                            page.insert_text(
                                rect.tl,
                                new_text,
                                fontsize=span["size"],
                                fontname="helv"
                            )

    doc.save(output_pdf)
    doc.close()


# تشغيل
replace_digits_in_pdf("book_0.pdf", "book_1.pdf")

print("خلصنا بدون تغيير التنسيق ✅")