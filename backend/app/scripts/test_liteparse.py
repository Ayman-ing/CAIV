from liteparse import LiteParse

parser = LiteParse(ocr_enabled=True)
result = parser.parse("/home/ayman-ing/study/projects/CAIV/backend/app/scripts/FekiAymanCV.pdf")
print(result.text)
