import re

text = "50  وكان ترتيب أخوه40 ترتيب محمد يف الصف هو"
# match:
q_match3 = re.search(r'(\d+)\s*وكان ترتيب أخوه\s*(\d+)\s*ترتيب (.*?)\s+(يف|في)\s+الصف\s+هو', text)
if q_match3:
    print(f"Match found! G1={q_match3.group(1)} (brother rank), G2={q_match3.group(2)} (person rank), G3={q_match3.group(3)} (name)")
    
    # translated = f"{q_match3.group(3)}'s rank in the class is {q_match3.group(2)} and his brother's rank is {q_match3.group(1)}"
    # print(translated)
else:
    print("No match.")

