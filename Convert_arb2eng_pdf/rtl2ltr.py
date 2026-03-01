import fitz  # PyMuPDF

def rtl_to_ltr_text(text):
    return text[::-1]  # قلب ترتيب الحروف


def convert_pdf_rtl_to_ltr(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)

    for page in doc:
        width = page.rect.width
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"]
                        reversed_text = rtl_to_ltr_text(original_text)

                        rect = fitz.Rect(span["bbox"])

                        # احسب مكان mirrored
                        new_x = width - rect.x1

                        # امسح النص القديم
                        page.add_redact_annot(rect, fill=(1, 1, 1))
                        page.apply_redactions()

                        # اكتب النص الجديد LTR
                        page.insert_text(
                            (new_x, rect.y0),
                            reversed_text,
                            fontsize=span["size"],
                            fontname="helv"
                        )

    doc.save(output_pdf)
    doc.close()


convert_pdf_rtl_to_ltr("book_0.pdf", "book_02.pdf")

print("تم التحويل من RTL إلى LTR ✅")