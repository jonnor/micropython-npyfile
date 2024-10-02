
[![Tests](https://github.com/jonnor/micropython-npyfile/actions/workflows/tests.yaml/badge.svg?branch=master)](https://github.com/jonnor/micropython-npyfile/actions/workflows/tests.yaml)

# micropython-npyfile

Support for [Numpy files (.npy)](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html) for [MicroPython](https://micropython.org/).
Simple persistence of multi-dimensional numeric array data, and interoperability with Numpy/CPython et.c.

Was initially written to be used with [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

#### Features

- Reading & writing .npy files with numeric data (see below for Limitations)
- Streaming/chunked reading & writing
- No external dependencies. Uses [array.array](https://docs.micropython.org/en/latest/library/array.html)
- Written in pure Python. Compatible with CPython, CircuitPython, et.c.


## Installing

This package can be installed using [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip).

For example:

```bash
mpremote mip install github:jonnor/micropython-npyfile
```

Or just copy the `npyfile.py` file to your MicroPython device.

## Usage

#### Save a file (simple)

```python

import array
import npyfile

shape = (10, 4)
data = array.array('f', (1.0 for _ in range(shape[0]*shape[1])))

npyfile.save('mydata.npy', data, shape)
```

#### Load a file (simple)

```python

import npyfile
shape, data = npyfile.load('mydata.npy')

print(shape)
print(data)
```

#### Streaming read

Streaming/chunked reading can be used to keep memory usage low.

```python
import npyfile

with npyfile.Reader('mydata.npy') as reader:

    # Metadata available on the reader object
    print(reader.shape, reader.typecode, reader.itemsize)

    # NOTE: assumes input is 2d. Pick chunksize in another way if not
    chunksize = reader.shape[1]
    for chunk in reader.read_data_chunks(chunksize):
        print(len(chunk), chunk)
```

More examples:

- Streaming matching data from two files: [two_streams.py](./examples/digits/two_streams.py)

#### Streaming write

Streaming/chunked writing can be used to keep memory usage low.

See implementation of `npyfile.save()`, in [npyfile.py](./npyfile.py)

#### Reading .npz files

.npz files are ZIP archives.
They can be read using an implementation of the zipfile module,
such as [jonnor/micropython-zipfile](https://github.com/jonnor/micropython-zipfile).
Both uncompressed and DEFLATE compressed files are supported.

For example code, see [read_npz.py](./examples/read_npz.py).

#### Saving portable files with numpy

numpy.save defaults to allowing pickle support.
This makes is very easy to accidentially save numpy.array
objects that use pickle for serialization, instead of just numeric data.
Such files will not be loadable by `npyfile` (or most other .npy readers).

To avoid this, when saving numeric arrays, always use:

```python
numpy.save(PATH, DATA, allow_pickle=False)
```


## Limitations

- Only little-endian is supported, not big-endian
- Only C data order is supported, not Fortran
- Strings are not supported
- Complex numbers not supported
- Pickled data is not supported

NOT TESTED on unsupported/malformed/malicious inputs.

## TODO 
Contributions welcomed!

TODO:

- Add tests for unsupported/malformed inputs

## Developing

#### Running tests on host

Install the Unix/Window port of MicroPython. Then run:

```
MICROPYPATH=./ micropython tests/test_npyfile.py
```

The tests can also be ran under CPython
```
PYTHONPATH=./ python tests/test_npyfile.py
```

#### Running tests on device

Connect a MicroPython device via USB.

Copy over the data
```
mpremote cp npyfile.py :
mpremote -r cp tests/ :
mpremote run tests/test_npyfile.py
```

