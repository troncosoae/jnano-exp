import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

from data_worker import combine_batches, split_into_batches, unpickle, \
    unpack_data, display_img
from tf_lib.Net import Net
from tf_lib.Interface import Interface
from tf_lib.data_worker import suit4tf


batches_names = [
    'data_batch_1', 'data_batch_2', 'data_batch_3', 'data_batch_4',
    'data_batch_5']


if __name__ == '__main__':
    print('running main')

    saved_weights_file = 'saved_nets/saved_tf/version1.pth'

    data_batches = [
        unpickle(f'datasets/cifar-10-batches-py/{batch_name}') for batch_name
        in batches_names]

    unpacked_batches = [
        (unpack_data(data_batch)) for data_batch
        in data_batches]

    print(unpacked_batches[0][0].shape)

    X, Y = combine_batches(unpacked_batches)

    print(X.shape, Y.shape)

    batches = split_into_batches(X, Y, 3)

    tf_batches = [(suit4tf(X, Y)) for X, Y in batches]

    X_tf = tf_batches[0][0]
    Y_tf = tf_batches[0][1]

    print(X_tf, Y_tf)

    # net = Net()
    # net.train([(X, Y)], 1, verbose=False, batch_size=None)

    # net.save_weights(saved_weights_file)

    # preds = net.predict(X_tf)
    # print('preds', preds)

    net = Sequential([
        layers.Conv2D(
            filters=6, kernel_size=5, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2), strides=2),
        layers.Conv2D(
            filters=16, kernel_size=5, padding='same', activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2), strides=2),
        layers.Flatten(),
        layers.Dense(120, activation='relu'),
        layers.Dense(84, activation='relu'),
        layers.Dense(10)
    ])
    net_interface = Interface(net)
    net_interface.train_net([(X, Y)], 1, verbose=False, batch_size=None)
    net_interface.save_weights(saved_weights_file)

    preds = net_interface.predict_net(X_tf)
    preds = preds.numpy()
    print(preds)
    print(np.argmax(preds, axis=1), Y_tf)
