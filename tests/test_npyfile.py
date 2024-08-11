
from npyfile import Reader, Writer, load, save


def test_reader_simple():

    with Reader('benchmarks/iir/noise.npy') as reader:
        print(reader.shape, reader.typecode, reader.itemsize)

        for s in reader.read_data_chunks(500):
            print(len(s))


def test_writer_simple():
    
    size = 100
    arr = array.array('f', (i for i in range(size)))
    shape = (size, )

    path = 'out.npy'

    # can be saved successfully
    save(path, arr, shape=shape)

    # can be loaded back up again
    loaded_shape, loaded_arr = load(path)
    assert loaded_shape == shape
    assert list(arr) == list(loaded_arr)

def main():
    test_reader_simple()
    test_writer_simple()


if __name__ == '__main__':
    main()

    # testcases
    # supported
    # super short file. Single value, or 2x2 array
    # common sizes and common formats. 1d/2d/3 uint8/int16/float

    # unsupported
    # object type
