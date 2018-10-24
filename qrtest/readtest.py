from PIL import Image
import pytesseract
# Note that tesseract will have to be installed (for Mac: brew install tesseract)

allText = pytesseract.image_to_string(Image.open('cover.jpg'), lang='eng')
if "REQUESTID" in allText:
    splitText = allText.split("REQUESTID")
    print(splitText[1].strip())
