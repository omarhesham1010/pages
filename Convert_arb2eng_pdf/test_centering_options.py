import fitz

doc = fitz.open("book_0.pdf")
page = doc[0]

# Strategy: get all drawings, find rectangles
paths = page.get_drawings()
shapes = []
for p in paths:
    r = p["rect"]
    # Filter very large/small paths
    if r.width < page.rect.width * 0.9 and r.width > 5 and r.height > 5:
        shapes.append(r)

def get_best_shape_for_rect(text_rect):
    # Find the shape that either contains this rect or has the highest intersection
    best_shape = None
    max_area = 0
    for s in shapes:
        if s.intersects(text_rect):
            intersect = s.intersect(text_rect)
            area = intersect.width * intersect.height
            if area > max_area:
                max_area = area
                best_shape = s
    return best_shape

def center_rect_in_shape(text_width, text_height, shape_rect):
    # Center X
    new_x0 = shape_rect.x0 + (shape_rect.width / 2.0) - (text_width / 2.0)
    # Center baseline Y
    # The font size represents approx height from top of shape to bottom of shape
    new_y0 = shape_rect.y0 + (shape_rect.height / 2.0) - (text_height / 2.0)
    return fitz.Rect(new_x0, new_y0, new_x0 + text_width, new_y0 + text_height)

# Check arabic letters against this logic
text_dict = page.get_text("dict")
for block in text_dict["blocks"]:
    if block["type"] != 0: continue
    for line in block["lines"]:
        for span in line["spans"]:
            txt = span["text"].strip()
            if txt in ["أ", "ب", "ج", "د"]:
                r = fitz.Rect(span["bbox"])
                print(f"Option '{txt}' found at {r}")
                
                # Assume translation turns this into "A", "B", "C", "D"
                # Let's say we have translated to "A" at fontsize = span['size']
                translated_txt = "A" if txt == "أ" else "B" if txt == "ب" else "C" if txt == "ج" else "D"
                font_size = span["size"]
                
                best_shape = get_best_shape_for_rect(r)
                if best_shape:
                    print(f"  -> Bounding shape: {best_shape}")
                    text_width = fitz.get_text_length(translated_txt, fontname='Times-Roman', fontsize=font_size)
                    
                    new_r = center_rect_in_shape(text_width, font_size, best_shape)
                    print(f"  -> Centered '{translated_txt}' at: {new_r}")
                else:
                    print(f"  -> No shape found for {txt}")
