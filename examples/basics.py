
# Simple write
import array
import npyfile

shape = (10, 4)
data = array.array('f', (1.0 for _ in range(shape[0]*shape[1])))

npyfile.save('mydata.npy', data, shape)


# Simple read
import npyfile

shape, data = npyfile.load('mydata.npy')

print(shape)
print(data)


# Streaming read
import npyfile

with npyfile.Reader('mydata.npy') as reader:

    # Metadata available on the reader object
    print(reader.shape, reader.typecode, reader.itemsize)

    # NOTE: assumes input is 2d. Pick chunksize in another way if not
    chunksize = reader.shape[1]
    for chunk in reader.read_data_chunks(chunksize):
        print(len(chunk), chunk)


# Streaming write
import npyfile
import array

with npyfile.Writer('output.npy', shape=(5, 3), typecode='f') as writer:
    chunk = array.array('f', (1.1, 2.2, 3.3))

    for i in range(5):
        writer.write_values(chunk, typecode='f')

data, shape = npyfile.load('output.npy')
print(shape)
print(data)
