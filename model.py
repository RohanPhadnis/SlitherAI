import random
import os
import numpy
from PIL import Image
from tensorflow import keras

file_list = os.listdir('data_v1')
master = []

for f in file_list:
    point = {}
    point['x'] = numpy.array(Image.open('data_v1/{}'.format(f))) / 255.
    point['y'] = f.replace('.png', '').split('_')
    point['y'] = numpy.array([int(n) for n in point['y']][1:])
    master.append(point)

RATIO = 0.75
random.shuffle(master)
BREAK = int(len(master) * RATIO)
training = master[:BREAK]
validation = master[BREAK:]

train_x = numpy.array([d['x'] for d in training])
train_y = numpy.array([d['y'] for d in training])
validation_x = numpy.array([d['x'] for d in validation])
validation_y = numpy.array([d['y'] for d in validation])

model = keras.models.Sequential([
    keras.layers.Conv2D(filters=16, kernel_size=(3, 3), activation='relu', input_shape=(600, 600, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(filters=32, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(filters=64, kernel_size=(3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(units=64, activation='relu'),
    keras.layers.Dense(units=32, activation='relu'),
    keras.layers.Dense(units=16, activation='relu'),
    keras.layers.Dense(units=3)
])

model.compile(optimizer='adam', loss='mse', metrics=['acc'])
model.summary()
model.fit(x=train_x, y=train_y, epochs=200, verbose=1, validation_data=(validation_x, validation_y))
model.save('data_v1/model.h5')