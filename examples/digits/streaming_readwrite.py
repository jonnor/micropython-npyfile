
"""
Example of reading from a file and writing to another, in a streaming fashion
"""

import npyfile
import array
import math

out_path = 'digits_features.npy'
n_features = 2 # mean, std

with npyfile.Reader('digits_data.npy') as data:

    # Check that data is expected format: n_samples x width x height, 1 byte each
    shape = data.shape
    assert shape[1:3] == (8, 8), shape
    assert data.itemsize == 1
    n_samples = shape[0]

    # preallocate reused feature-array
    features = array.array('f', (0.0 for _ in range(n_features)))
    # Open output stream, same number of rows as input
    with npyfile.Writer(out_path, shape=(n_samples, n_features), typecode='f') as outfile:

        # Read data one image at a time
        data_chunk = 8*8
        sample_count = 0

        data_chunks = data.read_data_chunks(data_chunk, offset=0)
        for arr in data_chunks:

            # compute features
            mean = sum(arr) / len(arr)
            variance = sum((x - mean) ** 2 for x in arr) / len(arr)
            std = math.sqrt(variance)

            # write it to file
            features[0] = mean
            features[1] = std
            outfile.write_values(features, typecode='f')          
            #print(features)

            sample_count += 1

        print('Processed', sample_count, 'rows')


    # Sanity check the output
    shape, features = npyfile.load(out_path)
    assert shape[0] == n_samples
    assert shape[1] == n_features
    print('Values for first samples')
    print(features[0:n_features*3])
