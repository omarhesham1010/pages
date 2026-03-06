import fitz

# Load the file to examine how PDF handles text widths
doc = fitz.open("book_0.pdf")
page = doc[0]

# Strategy: we need to calculate the bounding box of the TRANSLATED text.
# The `font_size` and `fontname` parameters are used for `insert_text`.
# fitz.get_text_length(text, fontname=..., fontsize=...) returns the width.

fontname = "Times-Roman"
fontsize = 12.0
text = "This is a test english sentence."
width = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
print(f"Width of '{text}' is: {width}")

# Algorithm Concept:
# per page, we gather all final replacements: (rect, translated, color_rgb, font_size)
# 
# 1. For each replacement, we generate the NEW bounding box:
#    new_width = fitz.get_text_length(translated, fontname=UNIFORM_FONT, fontsize=font_size)
#    new_x0 = rect.x0 + HORIZONTAL_OFFSET
#    new_y0 = rect.y0
#    new_x1 = new_x0 + new_width
#    new_y1 = rect.y1 (or y0 + font_size)
#
# 2. Sort all replacements on the page primarily by Y coordinate (top to bottom), 
#    and secondarily by X (left to right) - or rather, separate them into Left Half and Right Half.
#
#    page_middle = page.rect.width / 2
#    If rect.x0 < page_middle -> Left Column
#    If rect.x0 >= page_middle -> Right Column
#
# 3. For each column, we check for overlaps.
#    Since text flows horizontally, if `rect_A.y0` and `rect_B.y0` are very close 
#    (e.g., abs(rect_A.y0 - rect_B.y0) < font_size * 0.5), they are on the SAME LINE.
#
#    If they are on the same line, `new_rect_A` and `new_rect_B` might overlap.
#    Overlap happens if `new_rect_A.x1 > new_rect_B.x0` (assuming A is to the left of B).
#
#    If overlap:
#    `new_rect_B.x0 = new_rect_A.x1 + spacing` (push B to the right).
