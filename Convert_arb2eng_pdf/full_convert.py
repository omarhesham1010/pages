import fitz  # PyMuPDF
import re
from deep_translator import GoogleTranslator
from tqdm import tqdm

input_file = "/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_0.pdf"
output_file = "/home/omar-h/Repos/pages/Convert_arb2eng_pdf/book_01.pdf"


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
        16.0: 12.0,
        17.0: 15.0,
        18.0: 15.0,
        19.0: 15.0,
        31.0: 31.0
    }

    # 👈 قاموس الترجمات المخصصة (تقدر تضيف هنا أي كلمات عاوز تترجمها بنفسك)
    # خلي بالك إن الكلمة لازم تكون مطابقة تماماً، بدون مسافات زيادة
    CUSTOM_TRANSLATIONS = {
        "الحســــــاب": "Mathematics",
        "ب": "B",
        # ضيف أي كلمات تانية هنا بنفس الطريقة:
        # "الكلمة_العربي": "الترجمة_الإنجليزي",
    }

    for page in tqdm(doc, desc="جاري ترجمة الصفحات...", unit="صفحة"):
        text_dict = page.get_text("dict")
        replacements = []

        for block in text_dict["blocks"]:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                for span in line["spans"]:

                    text = span["text"]
                    clean_text = text.strip()
                    if not clean_text:
                        continue

                    # فحص الترجمة المخصصة
                    import re
                    
                    # دالة لتنظيف وتصحيح أخطاء استخراج النص العربي من الـ PDF
                    def normalize_arabic(text):
                        # إزالة التطويل
                        text = re.sub(r'ـ+', '', text)
                        # تصليح أخطاء شائعة في استخراج الـ PDF المنعكس (حرف الـ 'ل' والـ 'ح'/'م')
                        # كتير "الحساب" بتطلع "احلساب" أو "المعرفة" تطلع "املعرفة"
                        text = text.replace("احل", "الح")
                        text = text.replace("امل", "الم")
                        text = text.replace("اجل", "الج")
                        text = text.replace("اخل", "الخ")
                        # توحيد أشكال الهمزة للألف
                        text = re.sub(r'[أإآا]', 'ا', text)
                        return text.strip()

                    text_normalized = normalize_arabic(clean_text)
                    
                    translated = None

                    # تجهيز نسخة مبسطة من القاموس بدون همزات وتطويل للمقارنة
                    normalized_translations = {}
                    for k, v in CUSTOM_TRANSLATIONS.items():
                        norm_k = normalize_arabic(k)
                        normalized_translations[norm_k] = v

                    if text_normalized in normalized_translations:
                        translated = normalized_translations[text_normalized]
                    else:
                        # 2. فحص الأرقام والمعادلات الرياضية البحتة
                        # لو النص كله أرقام ورموز رياضية وفواصل، مفيش داعي نبعته لجوجل عشان بيبوظ الترتيب
                        if re.match(r'^[\d\s\.,،\-\+\*\/\^\(\)%:=]+$', clean_text):
                            math_text = span["text"]
                            math_text = math_text.replace('،', ',')
                            # بما أن اتجاه الرياضيات في العربي بيكون اليمين لليسار، الفاصلة بتكون في آخر النص
                            # لكن لما نكتب بالإنجليزي (يسار ليمين) محتاجين الفاصلة تكون في أول النص عشان تترسم صح
                            if re.search(r',\s*$', math_text):
                                math_text = re.sub(r'(.*?)(,\s*)$', r'\2\1', math_text)
                            translated = math_text
                        else:
                            # 3. محاولة التقاط أسئلة الرياضيات المعكوسة
                            # تحويل الأرقام العربية المشرقية إلى أرقام إنجليزية للمطابقة
                            ar_to_en = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
                            text_num_en = clean_text.translate(ar_to_en)
                            
                            # التقاط: "؟99  اىل3   كم عدد من" أو مشابهة
                            q_match1 = re.search(r'؟\s*(\d+)\s*(?:اىل|إلى|الي)\s*(\d+)\s*كم عدد من', text_num_en)
                            # التقاط: "؟ 99 ، 3 كم عدد محصور بني" أو مشابهة
                            q_match2 = re.search(r'؟\s*(\d+)\s*،\s*(\d+)\s*كم عدد محصور', text_num_en)
                            # التقاط أسئلة الترتيب المعكوسة
                            q_match3 = re.search(r'(\d+)\s*وكان ترتيب أخوه\s*(\d+)\s*ترتيب (.*?)\s+(يف|في)\s+الصف\s+هو', text_num_en)
                            
                            if q_match1:
                                translated = f"How many numbers are there from {q_match1.group(2)} to {q_match1.group(1)}?"
                            elif q_match2:
                                translated = f"How many numbers are there between {q_match2.group(2)} and {q_match2.group(1)}?"
                            elif q_match3:
                                try:
                                    name = translator.translate(q_match3.group(3))
                                except:
                                    name = q_match3.group(3)
                                translated = f"{name}'s rank in the class is {q_match3.group(2)} and his brother's rank was {q_match3.group(1)}"
                            else:
                                # 4. نترجم بجوجل الاول
                                try:
                                    # نترجم النص الأصلي
                                    translated = translator.translate(text)
                                    if translated:
                                        
                                        # هل في أي كلمة من القاموس كجزء من النص؟
                                        text_for_google = text_normalized
                                        custom_applied = False
                                        
                                        # ترتيب الكلمات المخصصة من الأطول للأقصر عشان نتجنب تداخل الحروف (مثل "ب" مع كلمة "حساب")
                                        for ar_word in sorted(normalized_translations.keys(), key=len, reverse=True):
                                            en_word = normalized_translations[ar_word]
                                            
                                            # نستخدم word boundaries عشان ما نبدلش حرف "ب" جوه كلمة زي "الحساب"
                                            # بس بما إن العربي معقد شوية، هنستخدم مسافات أو بداية ونهاية السطر
                                            # طريقة أبسط: لو الكلمة مساوية للنص بالكامل أو لو هي كلمة مستقلة
                                            pattern = r'(?:^|\s)' + re.escape(ar_word) + r'(?:\s|$)'
                                            if re.search(pattern, text_for_google):
                                                # استبدال الكلمة بالإنجليزية
                                                text_for_google = re.sub(pattern, f" {en_word} ", text_for_google)
                                                custom_applied = True
                                            # لو الكلمة مطابقة للنص جزئياً بدون مسافات (زي حرف 'ب') ممكن تعمل مشكلة
                                            # لكن خليناها تبحث عن الكلمة المستقلة فقط.

                                        if custom_applied:
                                            translated_custom = translator.translate(text_for_google)
                                            if translated_custom:
                                                translated = translated_custom
                                        
                                except:
                                    continue
                        
                        if not translated:
                            continue

                        # إذا كانت الكلمة جزء من جملة، يمكننا أيضاً استبدالها بعد الترجمة (اختياري)
                        # لكن الأفضل الاعتماد على الترجمة المخصصة للنصوص المنفصلة أولاً

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
                        t_lower = t.lower()
                        math_words = ['major', 'minor', 'large', 'small', 'big', 'الكبير', 'الصغير', 'الأكبر', 'الأصغر', 'كبير', 'صغير']
                        has_math_word = any(w in t_lower for w in math_words)
                        has_math_symbol = any(c in t for c in '=+-*/')
                        
                        if has_math_word and has_math_symbol:
                            t_new = t.replace('الكبير', 'Large').replace('الأكبر', 'Large').replace('big', 'Large').replace('major', 'Large').replace('Major', 'Large').replace('كبير', 'Large').replace('large', 'Large')
                            t_new = t_new.replace('الصغير', 'Small').replace('الأصغر', 'Small').replace('minor', 'Small').replace('Minor', 'Small').replace('صغير', 'Small').replace('small', 'Small')
                            
                            # Google translates isolated "= الكبير - الصغير - 1" into "Large = Small - 1"
                            t_new = re.sub(r'Large\s*=\s*Small', '= Large - Small', t_new)
                            
                            tokens = [tok.strip() for tok in re.split(r'([=+\-*/])', t_new) if tok.strip()]
                            
                            # Determine if we should reverse based on the position of the equals sign or layout
                            if t_new.strip().startswith('='):
                                # It's naturally left-to-right (very rare for Arabic PDF extraction of equations)
                                # but keep spacing unified.
                                return " ".join(tokens)
                            else:
                                tokens.reverse()
                                reversed_t = " ".join(tokens)
                                
                                # Google translates the messy extraction as "95 = 1 - 3 - 99 = 1 - Minor - = Major"
                                # Since it's completely backward, if we reverse it raw: "Major = - Minor - 1 = 99 - 3 - 1 = 95"
                                # We need to change "Major = - Minor" -> "= Major - Minor".
                                reversed_t = re.sub(r'(?i)Large\s*=\s*-\s*Small', '= Large - Small', reversed_t)
                                reversed_t = re.sub(r'(?i)Small\s*=\s*-\s*Large', '= Small - Large', reversed_t)
                                reversed_t = re.sub(r'(?i)Large\s*=\s*\+\s*Small', '= Large + Small', reversed_t)
                                reversed_t = re.sub(r'(?i)Small\s*=\s*\+\s*Large', '= Small + Large', reversed_t)
                                
                                # Sometimes parsing anomalies leave "Small - Large" which is mathematically wrong for these questions
                                reversed_t = re.sub(r'(?i)Small\s*-\s*Large', 'Large - Small', reversed_t)
                                
                                # If PyMuPDF extracts "الكبير = الصغير - 1" it gets reversed into "Large = Small - 1".
                                # The user wants these formulas formatted as "= Large - Small - 1".
                                reversed_t = re.sub(r'(?i)^Large\s*=\s*Small', '= Large - Small', reversed_t)
                                
                                return reversed_t
                            
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

        # 🚀 خوارزمية منع التداخل (Anti-Overlap)
        page_width = page.rect.width
        page_midpoint = page_width / 2.0
        
        # 1. تقسيم العناصر إلى عمودين (يمين ويسار) عشان ما نخلطش السطور
        left_col = []
        right_col = []
        for r in replacements:
            rect = r[0]
            if rect.x0 < page_midpoint:
                left_col.append(r)
            else:
                right_col.append(r)
                
        def shift_column_overlaps(col):
            if not col:
                return []
                
            # ترتيب من فوق لتحت الطولياً
            col.sort(key=lambda r: r[0].y0)
            
            lines = []
            current_line = []
            
            # تجميع العناصر اللي على نفس السطر المربع (تفاوت بسيط في حرف الـ Y)
            for r in col:
                rect = r[0] # Rect
                font_size = r[3]
                if not current_line:
                    current_line.append(r)
                    continue
                    
                prev_rect = current_line[-1][0]
                # لو الفرق في الـ Y صغير جداً (أقل من نصف حجم الخط)، فهما على نفس السطر
                if abs(rect.y0 - prev_rect.y0) < font_size * 0.5:
                    current_line.append(r)
                else:
                    lines.append(current_line)
                    current_line = [r]
            if current_line:
                lines.append(current_line)
                
            shifted_col = []
            for line in lines:
                # ترتيب العناصر داخل نفس السطر من اليسار لليمين
                line.sort(key=lambda r: r[0].x0)
                
                current_x_end = None
                
                for r in line:
                    rect, translated_text, color_rgb, font_size = r
                    
                    # هل مساحة النص ده هتدخل في المساحة بتاعة النص اللي قبليه؟
                    if current_x_end is not None and rect.x0 < current_x_end:
                        # ترحيل النص ده لليمين شوية عشان ما يخبطش في اللي قبله
                        shift_amount = current_x_end - rect.x0 + 3.0 # + مسافة 3 نقط أمان
                        rect.x0 += shift_amount
                        rect.x1 += shift_amount
                        
                    # حساب العرض الحقيقي للنص الإنجليزي بعد الترجمة
                    text_width = fitz.get_text_length(translated_text, fontname=UNIFORM_FONT, fontsize=font_size)
                    
                    # حفظ نهاية النص ده عشان نقارنه باللي بعده
                    current_x_end = rect.x0 + text_width
                    
                    shifted_col.append((rect, translated_text, color_rgb, font_size))
                    
            return shifted_col

        shifted_left = shift_column_overlaps(left_col)
        shifted_right = shift_column_overlaps(right_col)
        final_replacements = shifted_left + shifted_right

        # ✍ كتابة النص بنفس الفونت الموحد
        for rect, translated, color_rgb, font_size in final_replacements:

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

    def process_stream(doc, xref, width):
        try:
            raw = doc.xref_stream(xref).decode("utf-8", errors="ignore")
        except Exception:
            return
            
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
        if new_stream != raw:
            doc.update_stream(xref, new_stream.encode("utf-8"))

    for page in tqdm(doc, desc="جاري تعديل التخطيط...", unit="صفحة"):
        width = page.rect.width
        
        # 1. تطبيق النقل على محتوى الصفحة المباشر
        contents = page.get_contents()
        for xref in contents:
            process_stream(doc, xref, width)
            
        # 2. تطبيق النقل على أي عناصر Form XObjects (زي الهيدر والفوتر)
        for xo in page.get_xobjects():
            # xo عبارة عن (xref, name, invoker, bbox)
            xref = xo[0]
            if doc.xref_is_stream(xref):
                obj_str = doc.xref_object(xref)
                if '/Subtype /Form' in obj_str:
                    process_stream(doc, xref, width)

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