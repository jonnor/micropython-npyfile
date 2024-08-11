
"""
Example of reading matching items from two files, in a streaming fashion
"""

import npyfile

def plot_image(arr, width, height):

    for row in range(height):
        row_data = arr[row*width:(row+1)*width]
        for c in row_data:
            # print using ANSI escape codes, grayscale background
            colorcode = 232+c
            print(f"\033[48;5;{colorcode}m  \033[0m", end='')
        print()

with npyfile.Reader('digits_labels.npy') as labels:
    assert len(labels.shape) == 1

    skip_samples = 1

    with npyfile.Reader('digits_data.npy') as data:

        # Check that data is expected format: sample x width x height, 1 byte each
        shape = data.shape
        assert shape[1:3] == (8, 8), shape
        assert data.itemsize == 1

        # Number of labels should match number of data items
        assert data.shape[0] == labels.shape[0] 

        # Read data and label for one image at a time
        data_chunk = 8*8
        sample_count = 0

        label_chunks = labels.read_data_chunks(1, offset=1*skip_samples)
        data_chunks = data.read_data_chunks(data_chunk, offset=data_chunk*skip_samples)

        for l_arr, arr in zip(label_chunks, data_chunks):

            # do something with the data
            print('Image', l_arr)
            plot_image(arr, 8, 8)               

            sample_count += 1
            if sample_count > 10:
                break



