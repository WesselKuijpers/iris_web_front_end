from helpers.predict_helper import PredictHelper
import time
import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np
from keras import backend as K
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential
from keras.optimizers import SGD
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator


# TODO: More SOLID
class Trainer:
    def __init__(self, epochs, batch_size, train_dir, val_dir, width, height):
        self.epochs = epochs
        self.batch_size = batch_size
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.width = width
        self.height = height
        self.model = None

    def start(self):
        train_process = mp.Process(target=self.initialize_trainer)
        train_process.start()

    def initialize_trainer(self):
        model = self.load_model()
        train_datagen = self.train_data_generator()
        test_datagen = self.test_data_generator()
        train_generator = self.train_directory_flow(train_datagen)
        validation_generator = self.train_directory_flow(test_datagen)
        hist = self.train(model, train_generator, validation_generator)
        self.plot_graph(hist)

    def load_model(self):
        model = PredictHelper().load_model('fruit_iris_core/densenet_v2.h5py')
        return model

    def train_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20)

    def test_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20)

    def train_directory_flow(self, train_generator):
        return train_generator.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical')

    def validation_directory_flow(self, val_generator):
        return val_generator.flow_from_directory(
            self.val_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical')

    def train(self, model, train_generator, validation_generator):
        # try to train and save the model
        try:
            hist = model.fit_generator(
                generator=train_generator,
                steps_per_epoch=5516 // self.batch_size,
                epochs=self.epochs,
                validation_data=validation_generator,
                validation_steps=1883 // self.batch_size)

            model.save('saved_models/' +
                       str(int(time.time())) + 'finished.h5py')
        except KeyboardInterrupt:
            hist = None
            # if the process is interupted by the user save the interupted model
            model.save('saved_models/' +
                       str(int(time.time())) + 'interupted.h5py')
            print("\ninterupted model was saved")
        except:
            hist = None
            # re-raise the error on any other interuption
            raise
        finally:
            return hist

    def plot_graph(self, hist):
        if hist:
            accuracy = hist.history['acc']
            val_accuracy = hist.history['val_acc']
            loss = hist.history['loss']
            val_loss = hist.history['val_loss']
            epochs = range(len(accuracy))
            plt.plot(epochs, accuracy, 'ro', label='Training accuracy')
            plt.plot(epochs, val_accuracy, 'bo', label='Validation accuracy')
            plt.plot(epochs, accuracy, 'r')
            plt.plot(epochs, val_accuracy, 'b')

            plt.title('Training and validation accuracy')
            plt.legend()

            plt.figure()
            plt.plot(epochs, loss, 'ro', label='Training loss')
            plt.plot(epochs, val_loss, 'bo', label='Validation loss')
            plt.plot(epochs, loss, 'r')
            plt.plot(epochs, val_loss, 'b')
            plt.title('Training and validation loss')
            plt.legend()

            plt.show()
        else:
            print("No graph could be generated: DATA INCOMPLETE")
