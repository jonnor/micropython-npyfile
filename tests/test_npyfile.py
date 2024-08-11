
import array
import os
import gc

from npyfile import Reader, Writer, load, save
from npyfile import compute_items, find_section



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

    # Should be able to load
    loaded_shape, loaded_arr = load(path)

    # check shape correct
    assert loaded_shape == expect_shape

    # check data correct
    items = compute_items(loaded_shape)
    expect = list(range(items))
    # with int8 arange values starts wrapping around after 127
    max_compare = 126
    o = list(loaded_arr)[0:max_compare]
    e = expect[0:max_compare]
    assert o == e, (o, e)

    del o; del e;
    gc.collect()

    # try to write the data
    temp_dir = 'tests/out'
    save_path = temp_dir + '/' + 'out.npy'
    save(save_path, loaded_arr, shape=loaded_shape)

    # should also load correctly
    saved_shape, saved_arr = load(save_path)
    assert saved_shape == expect_shape

    o = list(saved_arr)[0:max_compare]
    e = expect[0:max_compare]
    assert o == e, (o, e)

def test_supported_files():
    data_dir = 'tests/data/supported'
    for filename in os.listdir(data_dir):
        #path = os.path.join(data_dir, filename)

        f = filename.encode('ascii')
        shape_str = find_section(f, b'(', b')')
        shape = tuple([ int(d) for d in shape_str.split(b',') ])

        path = data_dir + '/' + filename
        print('file', shape, filename)
        run_test_supported(path, shape)
        gc.collect()

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
