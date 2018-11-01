from PIL import Image
import pyzbar.pyzbar as pyzbar

filename = 'mycode'
decodedImg = pyzbar.decode(Image.open("./static/"+filename+".png"))[0].data.decode("utf-8")
print(decodedImg)
