# micropython-npyfile

Support for [Numpy files (.npy)](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html) for [MicroPython](https://micropython.org/).
Simple persistence of multi-dimensional numeric array data, and interoperability with Numpy/CPython et.c.

Was initially written to be used with [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

Features

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

## Usage

See the [tests](./tests)

`TODO: Add a couple of examples`

## Limitations

- Only little-endian is supported, not big-endian
- Only C data order is supported, not Fortran
- Strings are not supported
- Complex numbers not supported
- Pickled data is not supported


## TODO 
Contributions welcomed!

TODO:

- Example code for loading/writing .npz files (Zip archives with .npy files)


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
mprempte cp npyfile.py :
mpremote cp tests/ :
mpremote run tests/test_npyfile.py
```

