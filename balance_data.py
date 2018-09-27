
import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

train_data = np.load('training_data.npy')

lefts = []
rights = []
forwards = []

print len(train_data)
i=0
for data in train_data:
    img = data[0]
    img=(img>70).astype('uint8')*125
    cho=data[1]
    choice = data[1][1]
    print data[1]
    if choice<490:

        cho[0]=float(cho[0])/1024
        cho[1]=float(cho[1])/1024
        lefts.append([img,cho])
        
    elif choice>520:
        cho[0]=float(cho[0])/1024
        cho[1]=float(cho[1])/1024

        rights.append([img,cho])
    else:
        cho[0]=float(cho[0])/1024
        cho[1]=float(cho[1])/1024
        forwards.append([img,cho])
else:
    pass


forwards = forwards[:len(lefts)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]
print len(lefts), len(rights), len(forwards)

final_data = forwards + lefts + rights
shuffle(final_data)
print len(final_data)

np.save('train.npy', final_data)