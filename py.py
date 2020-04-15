import base64
from PIL import Image

# im = Image.open('lcdp.png')
# a = bytearray(im)
# b = base64.b64encode(im)
with open("lcdp.png", "rb") as image:
  f = image.read()
  b = bytearray(f)
  bs = base64.b64encode(b)
e = list((bs))

print((bs.decode()))