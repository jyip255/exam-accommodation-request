from pdf2image import convert_from_path

pdf_name = "FIND 2018 Performer Contract"

pages = convert_from_path(pdf_name + ".pdf", 500)

i = 1
for page in pages:
	page.save(pdf_name + str(i) + ".jpg", 'JPEG')
	i+=1