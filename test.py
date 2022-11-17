import subprocess
import base64

with open("./test/test.txt", "+rb") as file:
    b64=base64.b64encode(file.read())
with open("./test/text2.txt","wb") as output_file:
    output_file.write(base64.b64decode(b64))
