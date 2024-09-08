
# zipfile module must be installed using mip
# See for example https://github.com/jonnor/micropython-zipfile

import zipfile
print('zipfile', zipfile.__file__)

import npyfile

path = 'examples/digits/digits_combined.npz'
with zipfile.ZipFile(path) as archive:
    
    files = archive.namelist()
    files = [ f for f in files if f.endswith('.npy') ]
    print(files)

    for name in files:
        f = archive.open(name)
        s, v = npyfile.load(f)
        print('ss', s, len(v))
