
"""
Support for Numpy .npy files for MicroPython

References:
https://numpy.org/doc/stable/reference/generated/numpy.lib.format.html
https://numpy.org/doc/1.13/neps/npy-format.html#a-simple-file-format-for-numpy-arrays
"""

import struct 
import array

NPY_MAGIC = b'\x93NUMPY'

format_mapping = {
    # npy format => (array.array typecode, itemsize in bytes)
    # floating point
    b'f8': ('d', 8),
    b'f4': ('f', 4),

    # bytes
    b'i1': ('b', 1),
    b'u1': ('B', 1),

}

# find the correct array.array formats to use
# can unfortunately depend on platform
# In particular on 64 bit, the integers are 8 bytes, and on 32 bit they are 4
def array_typecode_itemsize(typecode):       
    arr = array.array(typecode, [0])
    b = bytes(arr)
    return len(b)   

for typecode in ['q', 'l', 'h', 'i']:
    size = array_typecode_itemsize(typecode)
    dummy = bytes(size)
    struct.unpack(typecode, dummy)
    key = f'i{size}'.encode('ascii')
    format_mapping[key] = (typecode, size)

for typecode in ['Q', 'L', 'H', 'I']:
    size = array_typecode_itemsize(typecode)
    dummy = bytes(size)
    struct.unpack(typecode, dummy)
    key = f'u{size}'.encode('ascii')
    format_mapping[key] = (typecode, size)


def find_section(data, prefix, suffix):
    start = data.index(prefix) + len(prefix)
    end = start + data[start:].index(suffix)

    section = data[start:end]
    return section

def array_tobytes_generator(arr):
    # array.array.tobytes() is missing in MicroPython =/
    typecode = array_typecode(arr)
    for item in arr: 
        buf = struct.pack(typecode, item)
        yield buf

def array_frombytes(typecode, buf):

    if True:
        arr = array.array(typecode, buf)
        return arr
    else:
        # XXX: dead code
        arr = array.array(typecode, buf)
        itemsize = len(buf) // len(arr)
        for idx in range(len(arr)):
            start = idx*itemsize
            arr[idx] = struct.unpack_from('<'+typecode, buf, start)[0]

        return arr

def array_typecode(arr):
    typecode = str(arr)[7:8]
    return typecode

def compute_items(shape):
    total_items = 1
    for d in shape:
        total_items *= d
    return total_items

class Reader():

    def __init__(self, filelike, header_maxlength=16*10):

        if isinstance(filelike, str):
            self.file = open(filelike, 'rb')
        else:
            self.file = filelike

        self.header_maxlength = header_maxlength

    def close(self):
        if self.file:
            self.file.close()
        self.file = None

    def __enter__(self):
        self._read_header()        
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def _read_header(self):

        # Read header data
        data = self.file.read(self.header_maxlength)

        # Check magic
        magic = data[0:len(NPY_MAGIC)] 
        assert magic == NPY_MAGIC, magic

        # Check version
        major, minor = struct.unpack_from('BB', data, len(NPY_MAGIC))
        if major == 0x01:
            header_length = struct.unpack_from('<H', data, len(NPY_MAGIC)+2)[0]
            header_start = len(NPY_MAGIC)+2+2
        elif major == 0x02:
            header_length = struct.unpack_from('<I', data, len(NPY_MAGIC)+2)[0]
            header_start = len(NPY_MAGIC)+2+4
        else:
            raise ValueError("Unsupported npy format version")

        #print('hs', header_start, data[header_start:header_start+header_length])

        # Parse header info
        type_info = find_section(data, b"'descr': '", b"',")
        type_endianess = type_info[0:1]
        # < is little-endian, | is not applicable (single byte values)
        assert type_endianess == b'<' or type_endianess == b'|', type_endianess
        type_format = type_info[1:]
        #print('tt', type_info)

        try:
            typecode, itemsize = format_mapping[type_format]
        except KeyError:
            raise ValueError(f"Unsupported data format: {type_format}")
        
        fortran_order = find_section(data, b"'fortran_order': ", b",")
        assert fortran_order == b'False', fortran_order # only C order supported

        shape_info = find_section(data, b"'shape': (", b"),")
        shape = tuple((int(d) for d in shape_info.split(b',') if d != b''))
        #print('ss', shape_info, shape)
        
        data_start = header_start + header_length
        assert (data_start % 16) == 0, data_start # should always be 16 bytes aligned

        self.typecode = typecode
        self.itemsize = itemsize
        self.shape = shape
        self.data_start = data_start

    def read_data_chunks(self, chunksize, offset=0):
        """
        Generator for reading data in chunks of specified size (in items)

        @offset is number of items to skip
        """

        # determine amount of data expected
        total_data_bytes = self.itemsize * compute_items(self.shape)

        # read the data
        self.file.seek(self.data_start + (self.itemsize*offset))

        chunksize_bytes = self.itemsize * chunksize
        #print('c', chunksize, chunksize_bytes, total_data_bytes)

        read_bytes = 0
        chunk_no = 0
        while read_bytes < total_data_bytes:
            sub = self.file.read(chunksize_bytes)
            arr = array_frombytes(self.typecode, sub)
            yield arr
            read_bytes += len(sub)
            chunk_no += 1
            #print('cc', chunk_no, read_bytes, total_data_bytes)


class Writer():
    def __init__(self, filelike, shape, typecode):

        if isinstance(filelike, str):
            self.file = open(filelike, 'wb')
        else:
            self.file = filelike

        self.typecode = typecode
        self.shape = shape

    def close(self):
        if self.file:
            self.file.close()
        self.file = None

    def __enter__(self):
        self._write_header()        
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def _write_header(self):
        shape = self.shape
        typecode = self.typecode

        # Sanity checking
        dimensions = len(shape)
        assert dimensions >= 1, dimensions
        assert dimensions <= 5, dimensions

        # Construct header info
        dtype_matches = [ key for key, (tc, size) in format_mapping.items() if tc == self.typecode ]
        assert len(dtype_matches) == 1, dtype_matches
        dtype = '<'+dtype_matches[0].decode('ascii')
        shape_str = ','.join((str(d) for d in shape))

        header = f"{{'descr': '{dtype}', 'fortran_order': False, 'shape': ({shape_str}), }}"
        #print('wh', header)
        
        # Padded to ensure data start is aligened to 16 bytes
        data_start = len(NPY_MAGIC)+2+2+len(header)
        padding = 16-(data_start % 16)
        header = header + (' ' * padding)
        header_length = len(header)
        data_start = len(NPY_MAGIC)+2+2+len(header)
        assert data_start % 16 == 0, data_start

        self.file.write(NPY_MAGIC)
        self.file.write(bytes([0x01, 0x00])) # version
        self.file.write(struct.pack('<H', header_length))
        header_data = header.encode('ascii')
        assert len(header_data) == len(header)
        self.file.write(header_data)

        # ready to write data

    def write_values(self, arr):
        input_typecode = array_typecode(arr)
        assert input_typecode == self.typecode, (input_typecode, self.typecode)

        for buf in array_tobytes_generator(arr):
            self.file.write(buf)


def load(filelike) -> tuple[tuple, array.array]:
    """
    Load array from .npy file

    Convenience function for doing it in one shot.
    For streaming, use npyfile.Reader instead
    """    

    chunks = []
    with Reader(filelike) as reader:
        # Just read everything in one chunk
        total_items = compute_items(reader.shape)
        for c in reader.read_data_chunks(total_items):
            chunks.append(c)

    assert len(chunks) == 1
    return reader.shape, chunks[0]

def save(filelike, arr : array.array, shape=None):
    """
    Save array as .npy file

    Convenience function for doing it in one shot.
    For streaming, use npyfile.Writer instead
    """

    if shape is None:
        # default to 1d
        shape = (len(arr), )        

    typecode = array_typecode(arr)
    total = compute_items(shape)
    assert total == len(arr), (shape, total, len(arr))

    with Writer(filelike, shape, typecode) as f:
        f.write_values(arr)


