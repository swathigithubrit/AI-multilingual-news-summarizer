# import re
# import spacy

# nlp = spacy.load("en_core_web_sm")

# KPI_PATTERNS = {
#     "Revenue": r"\b(revenue|revenues)\b",
#     "Profit": r"\b(profit|net income|earnings)\b",
#     "Loss": r"\b(loss|losses|negative earnings)\b",
#     "Free Cash Flow": r"\b(free cash flow|fcf)\b",
#     "YOY Growth (%)": r"\b(yoy growth|year[-\s]?on[-\s]?year|annual growth)\b",
#     "Sequential Growth (%)": r"\b(sequential growth|q[-\s]?o[-\s]?q|quarter[-\s]?on[-\s]?quarter)\b",
#     "Margin": r"\b(margin|operating margin|profit margin)\b",
#     "Deal Value": r"\b(deal|contract|tcv|total contract value)\b",
#     "Sales": r"\b(sales)\b",
#     "Guidance": r"\b(guidance|forecast|projection|estimate)\b",
#     "Headcount": r"\b(employee[s]?|headcount|staff)\b"
# }

# VALUE_PATTERN = r"(\$?\d[\d,\.]*\s?(million|billion|crore|lakh|%|percent)?)"

# def is_year_like(val):
#     clean = val.replace(",", "").replace("$", "").strip()
#     return clean.isdigit() and 2000 <= int(clean) <= 2100

# def is_percentage(val):
#     return "%" in val or "percent" in val.lower()

# def is_money(val):
#     return "$" in val or "million" in val.lower() or "billion" in val.lower() or "crore" in val.lower() or "lakh" in val.lower()

# def is_valid_value(val, kpi):
#     if not val or len(val.strip()) < 2:
#         return False
#     if is_year_like(val):
#         return False
#     if "Growth" in kpi or "%" in kpi:
#         return is_percentage(val)
#     if kpi in ["Revenue", "Profit", "Loss", "Sales", "Free Cash Flow", "Deal Value"]:
#         return is_money(val)
#     if kpi == "Headcount":
#         try:
#             return float(val.replace(",", "").replace("$", "")) < 1_000_000
#         except:
#             return False
#     return True

# def extract_kpis(text):
#     doc = nlp(text)
#     kpis = {}

#     for sent in doc.sents:
#         sentence = sent.text.strip()
#         for kpi_name, pattern in KPI_PATTERNS.items():
#             if re.search(pattern, sentence, re.IGNORECASE):
#                 values = re.findall(VALUE_PATTERN, sentence, re.IGNORECASE)
#                 for val in values:
#                     clean_val = val[0].strip()
#                     if is_valid_value(clean_val, kpi_name):
#                         if kpi_name not in kpis:
#                             kpis[kpi_name] = set()
#                         kpis[kpi_name].add(clean_val)

#     return [(kpi, val) for kpi, vals in kpis.items() for val in vals]
