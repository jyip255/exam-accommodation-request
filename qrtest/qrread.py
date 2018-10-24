from PIL import Image
import pyzbar.pyzbar as pyzbar

decodedImg = pyzbar.decode(Image.open('./static/mycode.png'))[0].data.decode("utf-8")
print(decodedImg)
