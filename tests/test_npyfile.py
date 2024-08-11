
import array
import os

from npyfile import Reader, Writer, load, save
from npyfile import compute_items, find_section


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


def run_test_supported(path, expect_shape):

    loaded_shape, loaded_arr = load(path)

    items = compute_items(loaded_shape)
    expect = list(range(items))

    assert loaded_shape == expect_shape
    assert list(loaded_arr)[0:126] == expect[0:126], (loaded_arr, expect)


def test_supported_files():
    data_dir = 'tests/data/supported'
    for filename in os.listdir(data_dir):
        #path = os.path.join(data_dir, filename)

        f = filename.encode('ascii')
        shape_str = find_section(f, b'(', b')')
        shape = tuple([ int(d) for d in shape_str.split(b',') ])

        #if not 'uint8' in filename:
        #    continue

        path = data_dir + '/' + filename
        print('file', shape, filename)
        run_test_supported(path, shape)

def main():
    tests = [
        #test_reader_simple,
        test_writer_simple,
        test_supported_files,
    ]
    for func in tests:
        print(func.__name__, '...')
        func()

    print('TESTS: OK')

if __name__ == '__main__':
    main()

    # testcases
    # supported
    # super short file. Single value, or 2x2 array
    # common sizes and common formats. 1d/2d/3 uint8/int16/float

    # unsupported
    # object type
