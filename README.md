# micropython-npyfile

Support for [Numpy files (.npy)](https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html) for [MicroPython](https://micropython.org/).
Simple persistence of multi-dimensional numeric array data, and interoperability with Numpy/CPython et.c.

Was initially written to be used with [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a Machine Learning and Digital Signal Processing library for MicroPython.

Features

- Reading & writing .npy files with numeric data (in C order)
- Streaming/chunked reading & writing
- No external dependencies. Uses [array.array](https://docs.micropython.org/en/latest/library/array.html)
- Compatible with CPython

TODO - contributions welcomed

- Example code for loading/writing .npz files (Zip archives with .npy files)

Unsupported - not planned

- Files with Fortran order
- Files with strings
- Files with pickled data

## Installing

This package can be installed using [mip](https://docs.micropython.org/en/latest/reference/packages.html#installing-packages-with-mip).

For example:

```bash
mpremote mip install github:jonnor/micropython-npyfile
```

## Usage

See the [tests](./tests)

`TODO: Add a couple of examples`

## Developing

`TODO: Document how to run tests`
