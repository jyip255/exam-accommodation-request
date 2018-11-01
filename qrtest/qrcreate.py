import pyqrcode
import png

filename = "mycode"
data = "yourapp.uconn.edu/exam_requests/<exam_request_id>"

qr = pyqrcode.create(data)
qr.png("./static/"+filename+".png", scale=6)
