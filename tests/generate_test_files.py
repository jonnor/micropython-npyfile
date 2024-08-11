
"""
Generate .npy files for testing

Intended to run in CPython
"""

import os
import itertools

import numpy


def generate_supported(out_dir):

    # Ref https://numpy.org/doc/stable/reference/arrays.dtypes.html
    dtypes = [
        # floating point
        numpy.float32,
        numpy.float64,
        'f',
        'f4',
        'f8',
        'd',
        # 8-bit integers
        numpy.uint8,
        'b',
        'B',
        # integers
        numpy.int32,
        'i',
        #'u',
        'i4',
        'u4',
        # 16-bit
        numpy.int16,
        'i2',
        'u2',
    ]

    shapes = [
        (133, ),
        (32, 32),
        (5, 16, 16),
        (4, 5, 7, 7),
    ]

    for dtype, shape in zip(dtypes, itertools.cycle(shapes)):

        shape_str = '(' + ','.join(str(d) for d in shape) + ')'

        items = numpy.cumprod(shape)[-1]
        data = numpy.arange(items, dtype=dtype).reshape(shape)

        dtype_str = dtype
        if 'type' in str(type(dtype)):
            dtype_str = repr(dtype).lstrip("<class '").rstrip("'>")

        name = f'{dtype_str}_{shape_str}.npy'
        print(name)
        path = os.path.join(out_dir, name)

        numpy.save(path, data)


def generate_unsupported():

    # unsupported.
    # complex numbers
    # unicode strings
    # zero-terminated strings
    # Python objects
    # raw data
    # timedelta
    # datetime
    # Structured fields
    # Big endian
    # boolean
    pass


def main():
    
    generate_supported('tests/data/supported')

if __name__ == '__main__':
    main()

