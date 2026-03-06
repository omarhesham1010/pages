"""
pdf_to_word.py
==============
يحول PDF إلى Word (.docx) مع الحفاظ على الـ layout والتصميم
باستخدام مكتبة pdf2docx المخصصة لهذا الغرض.

الاستخدام:
    python pdf_to_word.py
    python pdf_to_word.py input.pdf output.docx
    python pdf_to_word.py input.pdf output.docx 1 10   ← أول 10 صفحات
"""

import sys
import os
from pdf2docx import Converter
import fitz

# ===== إعدادات =====
INPUT_PDF   = os.path.join(os.path.dirname(__file__), "Math_Book_00.pdf")
OUTPUT_DOCX = os.path.join(os.path.dirname(__file__), "Math_Book_00.docx")

# رينج الصفحات (None = كل الصفحات)
START_PAGE = None   # مثال: 0  (0-indexed)
END_PAGE   = None   # مثال: 10
# ====================


def convert(input_pdf: str, output_docx: str,
            start: int = None, end: int = None):

    # حساب مجموع الصفحات
    doc = fitz.open(input_pdf)
    total = doc.page_count
    doc.close()

    # pdf2docx بيستخدم 0-indexed ولا يقبل None
    page_start = start if start is not None else 0
    page_end   = end   if end   is not None else total

    if not (0 <= page_start < total and page_start < page_end <= total):
        raise ValueError(
            f"رينج غلط: ({page_start}, {page_end}). الملف فيه {total} صفحة."
        )

    print(f"📄 {os.path.basename(input_pdf)}")
    print(f"   الصفحات: {page_start + 1} → {page_end}  (من إجمالي {total})")
    print(f"   → {os.path.basename(output_docx)}")
    print()

    cv = Converter(input_pdf)
    cv.convert(
        output_docx,
        start=page_start,
        end=page_end,
        # خيارات لتحسين الدقة
        connected_border_tolerance=0.5,  # دقة الحدود
        line_overlap_threshold=0.9,
        line_merging_threshold=2,
    )
    cv.close()

    size_mb = os.path.getsize(output_docx) / (1024 * 1024)
    print(f"✅ تم الحفظ: {output_docx}")
    print(f"   الحجم: {size_mb:.2f} MB")


if __name__ == "__main__":
    # دعم تشغيل من الكومند لاين
    if len(sys.argv) >= 3:
        INPUT_PDF   = sys.argv[1]
        OUTPUT_DOCX = sys.argv[2]
    elif len(sys.argv) == 2:
        INPUT_PDF   = sys.argv[1]
        OUTPUT_DOCX = os.path.splitext(INPUT_PDF)[0] + ".docx"

    if len(sys.argv) == 5:
        START_PAGE = int(sys.argv[3]) - 1  # تحويل من 1-indexed لـ 0-indexed
        END_PAGE   = int(sys.argv[4])

    convert(INPUT_PDF, OUTPUT_DOCX, START_PAGE, END_PAGE)
