# train_model.py
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
import numpy as np
from alexnet import alexnet
WIDTH = 200
HEIGHT = 150
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'ROS-car-fast-{}-{}-{}-epochs-data.model'.format(LR, 'alexnetv2',EPOCHS)

model = alexnet(WIDTH, HEIGHT, LR)

hm_data = 22
for j in range(EPOCHS):
    for i in range(1,hm_data+1):
        train_data = np.load('training_data.npy'.format(i))
        print j,i

        train = train_data[:-100]
        test = train_data[-100:]

        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,3)
        Y = [i[1] for i in train]
        # Z = [i[2] for i in train]
        print len(X), len(Y)

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,3)
        test_y = [i[1] for i in test]
        # test_z = [i[2] for i in test]
        print "hh"

        # model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),snapshot_step=100, show_metric=True, run_id=MODEL_NAME)
        model.fit(X, Y, n_epoch =1 , validation_set=(test_x, test_y), show_metric=True, batch_size=32)
        model.save(MODEL_NAME)
        print 'saved'



# tensorboard --logdir=/log
