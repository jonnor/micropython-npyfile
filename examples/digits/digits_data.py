
import numpy
from sklearn.datasets import load_digits

digits = load_digits(n_class=10)

#X = X.reshape((-1, 8, 8)).astype(numpy.uint8)
X = digits.images.astype(numpy.uint8)
Y = digits.target.astype(numpy.uint8)
print(X.shape, X.dtype)
print(Y.shape, Y.dtype)

numpy.save('digits_data.npy', X)
numpy.save('digits_labels.npy', Y)
