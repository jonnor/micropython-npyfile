
import array
import npyfile

shape = (10, 4)
data = array.array('f', (1.0 for _ in range(shape[0]*shape[1])))

npyfile.save('mydata.npy', data, shape)


import npyfile
shape, data = npyfile.load('mydata.npy')

print(shape)
print(data)


import npyfile

with npyfile.Reader('mydata.npy') as reader:

    # Metadata available on the reader object
    print(reader.shape, reader.typecode, reader.itemsize)

    # NOTE: assumes input is 2d. Pick chunksize in another way if not
    chunksize = reader.shape[1]
    for chunk in reader.read_data_chunks(chunksize):
        print(len(chunk), chunk)
