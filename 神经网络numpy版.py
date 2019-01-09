
# -- coding:utf-8 --
import numpy as np

train_x = np.array([
    [0, 0, 1],
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 0, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 0]
])
train_y = np.array([
    [0],
    [1],
    [1],
    [0],
    [0],
    [0],
    [0],
    [0]
])


def _sigmoid(x, der=False):

    if der is True:
        return x * (1 - x)

    return 1 / (1 + np.exp(-x))


def _tanh(x, der=False):

    if der is True:
        return 1 - (x * x)

    return np.tanh(x)


def _relu(x, der=False):

    if der is True:
        return 1 * (x > 0)

    return x * (x > 0)


def train():

    i = 3
    o = 1

    # hyperparameter
    num = 50000
    h = 4

    # parameter
    syn0 = 2 * np.random.random((i, h)) - 1
    syn1 = 2 * np.random.random((h, o)) - 1

    for epoch in range(num):

        # feed forward
        l0 = train_x                                        # (8,i)
        l1 = _sigmoid(l0.dot(syn0))              # (8,i) (i,h) (8,h)
        l2 = _sigmoid(l1.dot(syn1))              # (8,h) (h,o) (8,o)

        # loss
        loss = 1 / 2 * (train_y - l2)**2         # (8,o)

        # back propagate
        l2_err = train_y - l2                    # (8,o)
        l2_delta = l2_err * _sigmoid(l2, der=True)  # (8,o) (8,o) (8,o)
        l1_err = l2_delta.dot(syn1.T)            # (4,h)
        l1_delta = l1_err * _sigmoid(l1, der=True)  # (4,h)

        # update parameter
        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

        if epoch % 1000 == 0:
            print(np.mean(loss))

    return syn0, syn1


def inference(syn0, syn1, x):

    l0 = x                                   # (4,i)
    l1 = _sigmoid(l0.dot(syn0))              # (4,h)
    l2 = _sigmoid(l1.dot(syn1))              # (4,o)

    return l2


test_x = np.array([0, 1, 1])

syn0, syn1 = train()
pre_y = inference(syn0, syn1, test_x)
print(pre_y)
