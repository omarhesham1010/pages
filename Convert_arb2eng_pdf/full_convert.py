import fitz  # PyMuPDF
import re
from deep_translator import GoogleTranslator

input_file = "book_0.pdf"
output_file = "book_00.pdf"


# ====== نسخ المحتوى ======
def copy(input_path):
    doc = fitz.open(input_path)
    return doc


# ====== translate =====
import fitz
import re
from deep_translator import GoogleTranslator

def translate_pdf_low_level___(input_path):
    doc = fitz.open(input_path)
    translator = GoogleTranslator(source='ar', target='en')

    for page in doc:
        contents = page.get_contents()

        for xref in contents:
            raw = doc.xref_stream(xref).decode("utf-8", errors="ignore")

            # نمسك النص داخل ( ... ) قبل Tj
            def replace_text(match):
                print(raw)
                return
                original_text = match.group(1)

                try:
                    translated = translator.translate(original_text)
                except:
                    translated = original_text  # لو فشل

                # نحط النص المترجم جوه نفس الأقواس
                return f"({translated}) Tj"

            new_stream = re.sub(
                r"\((.*?)\)\s*Tj",
                replace_text,
                raw
            )

            doc.update_stream(xref, new_stream.encode("utf-8"))

    return doc

def translate_pdf_low_level_detection(input_path):
    doc = fitz.open(input_path)

    for page in doc:
        contents = page.get_contents()

        for xref in contents:
            raw = doc.xref_stream(xref).decode("latin1")

            # 1️⃣ شيل ( ... ) Tj
            raw = re.sub(
                r"\([^)]*\)\s*Tj",
                "",
                raw
            )

            # 2️⃣ شيل Arrays اللي فيها نص فقط قبل TJ
            raw = re.sub(
                r"\[(?:[^\]]*\([^)]*\)[^\]]*)\]\s*TJ",
                "",
                raw
            )

            doc.update_stream(xref, raw.encode("latin1"))

    return doc

def translate_pdf_low_level(input_path):
    doc = fitz.open(input_path)

    for page in doc:
        contents = page.get_contents()

        for xref in contents:
            raw = doc.xref_stream(xref).decode("latin1")

            # 🔥 استبدال النص داخل الأقواس فقط
            def mask_text(match):
                text = match.group(1)

                new_text = ""

                for ch in text:
                    if ch.isdigit():
                        new_text += "0"
                    elif ch.strip() == "":
                        new_text += ch  # نحافظ على المسافات
                    else:
                        new_text += "A"

                return f"({new_text})"

            raw = re.sub(
                r"\((.*?)\)",
                mask_text,
                raw,
                flags=re.DOTALL
            )

            doc.update_stream(xref, raw.encode("latin1"))

    return doc

def remove_all_text_with_display(input_path):
    doc = fitz.open(input_path)

    for page_number, page in enumerate(doc):
        streams = page.get_contents()

        for xobj in page.get_xobjects():
            streams.append(xobj[0])

        for xref in streams:
            try:
                raw = doc.xref_stream(xref).decode("latin1")

                print(f"\n========== PAGE {page_number} | XREF {xref} ==========")

                # --- Tj ---
                def show_tj(match):
                    print("Removing Tj  :", match.group(0))
                    return ""

                raw = re.sub(r"\([^)]*\)\s*Tj", show_tj, raw)
                raw = re.sub(r"\([^)]*\)Tj", show_tj, raw)

                # --- TJ ---
                def show_TJ(match):
                    print("Removing TJ  :", match.group(0))
                    return ""

                raw = re.sub(r"\[[^\]]*\]\s*TJ", show_TJ, raw)
                raw = re.sub(r"\[[^\]]*\]TJ", show_TJ, raw)

                # --- Hex Tj ---
                def show_hex(match):
                    print("Removing HEX :", match.group(0))
                    return ""

                raw = re.sub(r"<[0-9A-Fa-f]+>\s*Tj", show_hex, raw)
                raw = re.sub(r"<[0-9A-Fa-f]+>Tj", show_hex, raw)

                # --- ActualText ---
                def show_actual(match):
                    print("Removing ActualText :", match.group(0))
                    return ""

                raw = re.sub(r"/ActualText<[^>]+>", show_actual, raw)

                doc.update_stream(xref, raw.encode("latin1"))

            except Exception as e:
                print("Error on xref", xref, ":", e)

    return doc

def display_real_text(input_path):
    doc = fitz.open(input_path)

    for page_number, page in enumerate(doc):
        print(f"\n===== PAGE {page_number} =====")

        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4]
            if text.strip():
                print(text)

    doc.close()

def translate_pdf_display_english(input_path):
    doc = fitz.open(input_path)
    translator = GoogleTranslator(source='ar', target='en')

    for page_number, page in enumerate(doc):
        print(f"\n===== PAGE {page_number} =====")

        blocks = page.get_text("blocks")

        for block in blocks:
            text = block[4]

            if text.strip():
                try:
                    translated = translator.translate(text)
                    print(translated)
                except:
                    print(text)

    doc.close()

def translate_pdf_span_level(input_path):
    doc = fitz.open(input_path)
    translator = GoogleTranslator(source='ar', target='en')

    for page in doc:

        text_dict = page.get_text("dict")
        replacements = []

        for block in text_dict["blocks"]:

            if block["type"] != 0:
                continue  # نص فقط

            for line in block["lines"]:
                for span in line["spans"]:

                    text = span["text"]

                    if not text.strip():
                        continue

                    try:
                        translated = translator.translate(text)
                    except:
                        continue

                    rect = fitz.Rect(span["bbox"])
                    font_size = span["size"]

                    replacements.append((rect, translated, font_size))

                    page.add_redact_annot(rect, fill=(1,1,1))

        page.apply_redactions()

        for rect, translated, font_size in replacements:
            page.insert_textbox(
                rect,
                translated,
                fontsize=font_size,   # نحافظ على نفس الحجم
                fontname="helv",
                color=(0,0,0),
                align=0
            )

    return doc

def translate_pdf_debug(input_path):
    doc = fitz.open(input_path)
    translator = GoogleTranslator(source='ar', target='en')

    for page_number, page in enumerate(doc):

        print(f"\n===== PAGE {page_number} =====")

        text_dict = page.get_text("dict")
        replacements = []

        for block in text_dict["blocks"]:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:

                    text = span["text"]

                    if not text.strip():
                        continue

                    print("AR:", text)

                    try:
                        translated = translator.translate(text)
                        print("EN:", translated)
                    except Exception as e:
                        print("ERROR:", e)
                        continue

                    rect = fitz.Rect(span["bbox"])
                    size = span["size"]

                    replacements.append((rect, translated, size))

                    page.add_redact_annot(rect, fill=(1,1,1))

        page.apply_redactions()

        for rect, translated, font_size, color_rgb in replacements:

            # نحسب baseline تقريبي
            x = rect.x0
            y = rect.y0 + font_size  # baseline

            page.insert_text(
                (x, y),
                translated,
                fontsize=12,
                fontname="helv",
                color=color_rgb
            )

            print("Insert result:", result)

    return doc

def translate_pdf_uniform_font(input_path):
    doc = fitz.open(input_path)
    translator = GoogleTranslator(source='ar', target='en')

    UNIFORM_FONT = "Times-Roman"  # 👈 تقدر تغيره
    UNIFORM_SIZE = 12             # 👈 تقدر تثبته أو تخليه span["size"]

    for page in doc:
        text_dict = page.get_text("dict")
        replacements = []

        for block in text_dict["blocks"]:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:

                    text = span["text"]
                    if not text.strip():
                        continue

                    try:
                        translated = translator.translate(text)
                    except:
                        continue

                    rect = fitz.Rect(span["bbox"])

                    # 🎨 لون النص الأصلي
                    color_int = span["color"]
                    r = (color_int >> 16) & 255
                    g = (color_int >> 8) & 255
                    b = color_int & 255
                    color_rgb = (r/255, g/255, b/255)

                    replacements.append((rect, translated, color_rgb))

                    page.add_redact_annot(rect)

        page.apply_redactions()

        # ✍ كتابة النص بنفس الفونت الموحد
        for rect, translated, color_rgb in replacements:

            x = rect.x0
            y = rect.y0 + UNIFORM_SIZE

            page.insert_text(
                (x, y),
                translated,
                fontsize=UNIFORM_SIZE,
                fontname=UNIFORM_FONT,
                color=color_rgb
            )

    return doc

# ====== layout =====
def simple_shift_by_type(input_path):
    doc = fitz.open(input_path)

    for page in doc:
        contents = page.get_contents()
        width = page.rect.width

        for xref in contents:
            raw = doc.xref_stream(xref).decode("utf-8", errors="ignore")
            lines = raw.split("\n")

            depth = 0  # لمتابعة nested q/Q
            new_lines = []

            for line in lines:

                stripped = line.strip()

                # ---- Track nesting ----
                if re.match(r"^\s*q\b", line):
                    depth += 1

                if re.match(r"^\s*Q\b", line):
                    depth = max(depth - 1, 0)

                # ---- Td (Text space) ----
                td_match = re.search(r"(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+Td", line)
                if td_match:
                    new_line = line
                    new_lines.append(new_line)
                    continue

                # ---- Tm (Text matrix) ----
                tm_match = re.search(r"(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+Tm", line)
                if tm_match:
                    a,b,c,d,e,f = map(float, tm_match.groups())
                    new_a = -a
                    new_c = -c
                    new_e_value = width - e
                    new_line = f"{new_a} {b} {new_c} {d} {new_e_value} {f} Tm"
                    new_lines.append(new_line)
                    continue

                # ---- cm (Graphics space) ----
                cm_match = re.search(
                    r"(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+(-?\d+\.?\d*)\s+cm",
                    line
                )
                if cm_match:
                    a_str, b_str, c_str, d_str, e_str, f_str = cm_match.groups()

                    a = float(a_str)
                    c = float(c_str)
                    e = float(e_str)

                    # نفس عدد الخانات العشرية بتاعة e
                    if "." in e_str:
                        decimal_places = len(e_str.split(".")[1])
                    else:
                        decimal_places = 0

                    new_a = -a
                    new_c = -c
                    new_e_value = width - e
                    new_e = f"{new_e_value:.{decimal_places}f}"


                    new_line = f"q {new_a} {b_str} {new_c} {d_str} {new_e} {f_str} cm"
                    
                    new_lines.append(new_line)
                    continue

                new_lines.append(line)

            new_stream = "\n".join(new_lines)
            doc.update_stream(xref, new_stream.encode("utf-8"))

    return doc


# ====== حفظ الملف ======
def save_pdf(doc, output_path):
    doc.save(output_path)
    doc.close()
    return output_path


# ====== التنفيذ ======
document = copy(input_file)
# document = simple_shift_by_type(document)
document = translate_pdf_uniform_font(document)
result_path = save_pdf(document, output_file)
print("تم الحفظ في:", result_path, "✅")