import keras 
from keras.models import Sequential 
from keras.layers import Convolution2D as Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense , Activation , Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD , Adam
from keras.losses import categorical_crossentropy,binary_crossentropy
train_datagen = ImageDataGenerator(
        rescale=1./255,
)
X_train=train_datagen.flow_from_directory('X',
                                                 target_size = (100, 100),
                                                 batch_size = 20,
                                                 class_mode = 'categorical')
def build_model():
    model = Sequential()
    # add Convolutional layers
    model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same',
                     input_shape=(100, 100, 3)))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2,2)))    
    model.add(Flatten())
    # Densely connected layers
    model.add(Dense(128, activation='relu'))
    # output layer
    model.add(Dense(4, activation='softmax'))
    # compile with adam optimizer & categorical_crossentropy loss function
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

model = build_model()
filepath='weights0.{epoch:02d}-{accuracy:.2f}.hdf5'
CB=keras.callbacks.ModelCheckpoint(filepath, monitor='accuracy', verbose=0, save_best_only=True, save_weights_only=False, mode='auto', period=1)
history =model.fit(X_train,epochs=3, callbacks=[CB])
model.save('my_model.h5') 