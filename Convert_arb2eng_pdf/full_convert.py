import fitz  # PyMuPDF
import re
from deep_translator import GoogleTranslator

input_file = "/run/media/omar-h/38029BDD029B9E86/Repos/pages/Convert_arb2eng_pdf/book_0.pdf"
output_file = "/run/media/omar-h/38029BDD029B9E86/Repos/pages/Convert_arb2eng_pdf/book_004.pdf"


# ====== نسخ المحتوى ======
def copy(input_path):
    doc = fitz.open(input_path)
    return doc


# ====== translate =====
def translate_pdf_uniform_font(input_path):
    if isinstance(input_path, str):
        doc = fitz.open(input_path)
    else:
        doc = input_path
    translator = GoogleTranslator(source='ar', target='en')

    UNIFORM_FONT = "Times-Roman"  # 👈 تقدر تغيره
    VERTICAL_OFFSET = 2           # 👈 مسافة بسيطة لإنزال النص وتوسيطه عمودياً (زودها أو نقصها حسب الحاجة)
    HORIZONTAL_OFFSET = 0         # 👈 مسافة بسيطة لدفع النص يميناً (زودها أو نقصها حسب الحاجة)

    # 👈 قاموس أحجام الخطوط. دي كل الأحجام اللي موجودة في الصفحة بالتقريب.
    # تقدر تغير الرقم اللي على اليمين (حجم الخط الإنجليزي) زي ما تحب:
    FONT_SIZE_MAP = {
        8.7: 8.7,
        12.0: 12.0,
        13.0: 13.0,
        14.0: 14.0,
        15.0: 12.0,
        16.0: 15.0,
        17.0: 15.0,
        18.0: 15.0,
        19.0: 15.0,
        31.0: 31.0
    }

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
                    
                    if not translated:
                        continue

                    # حل مشكلة النقطة والـ (:) بدون استخدام رموز Unicode بتظهر كنقطة (·)
                    # المشكلة بتحصل لما الترجمة بتبدأ أو تنتهي بعلامات ترقيم.
                    # هنشيل علامات الترقيم من أول النص (لو جات بالغلط بسبب اتجاه العربي) ونحطها في الآخر
                    import re
                    match = re.search(r'^([.:!?]+)(.*)$', translated.strip())
                    if match:
                        translated = match.group(2).strip() + match.group(1)

                    # حل مشكلة المعادلات الرياضية اللي بتترجم بالمقلوب
                    # لو النص عبارة عن معادلة رياضية بشكل كبير، هنعكس ترتيب الكلمات بتاعته 
                    def fix_math(t):
                        if '=' in t and sum(1 for c in t if c in '0123456789=+-*/%()') > len(t) * 0.2:
                            return " ".join(reversed(t.split()))
                        return t
                    
                    translated = fix_math(translated)

                    rect = fitz.Rect(span["bbox"])

                    # 🎨 لون النص الأصلي
                    color_int = span["color"]
                    r = (color_int >> 16) & 255
                    g = (color_int >> 8) & 255
                    b = color_int & 255
                    color_rgb = (r/255, g/255, b/255)

                    original_size = round(span["size"], 1)
                    font_size = FONT_SIZE_MAP.get(original_size, original_size)

                    replacements.append((rect, translated, color_rgb, font_size))

                    page.add_redact_annot(rect)

        page.apply_redactions()

        # ✍ كتابة النص بنفس الفونت الموحد
        for rect, translated, color_rgb, font_size in replacements:

            x = rect.x0 + HORIZONTAL_OFFSET
            y = rect.y0 + font_size + VERTICAL_OFFSET

            page.insert_text(
                (x, y),
                translated,
                fontsize=font_size,
                fontname=UNIFORM_FONT,
                color=color_rgb
            )

    return doc

# ====== layout =====
def simple_shift_by_type(input_path):
    if isinstance(input_path, str):
        doc = fitz.open(input_path)
    else:
        doc = input_path

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
# ترتيب التشغيل مهم جداً: يجب تطبيق تغيير الاتجاه (shift) أولاً
# ثم تطبيق الترجمة (translate) حتى لا يتم عكس النص الإنجليزي
document = copy(input_file)
document = simple_shift_by_type(document)
document = translate_pdf_uniform_font(document)
result_path = save_pdf(document, output_file)
print("تم الحفظ في:", result_path, "✅")