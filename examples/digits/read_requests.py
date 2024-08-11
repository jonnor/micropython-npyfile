
import io
import requests
import npyfile

url = 'https://raw.githubusercontent.com/jonnor/micropython-npyfile/master/examples/digits/digits_labels.npy'

r = requests.get(url)
assert r.status_code == 200

shape, data = npyfile.load(io.BytesIO(r.content))
print(shape, data)
