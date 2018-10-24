import pyqrcode
import png
from PIL import Image

filename = "./static/mycode"
qr = pyqrcode.create("https://yourapp.uconn.edu/exam_requests/<exam_request_id>")
qr.png(filename+".png", scale=6)
im = Image.open(filename+".png")
new_im = im.convert('RGB')
new_im.save(filename+".jpg")
