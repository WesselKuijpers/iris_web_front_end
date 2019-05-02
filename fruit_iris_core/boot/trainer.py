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
import json
from flask import current_app as app


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

    def start(self, event):
        # e.unset()
        train_process = mp.Process(target=self.initialize_trainer, args=(event,))
        train_process.start()

    def initialize_trainer(self, event):
        while True:
            # configuring the Tensorflow option to consume only a limited amount of GPU memory
            # pass it to keras as the current session
            # this is done to prevent OOM errors
            gpu_options = tf.GPUOptions(
                per_process_gpu_memory_fraction=0.7, allow_growth=True)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
            K.set_session(sess)
            
            model = self.load_model()
            train_datagen = self.train_data_generator()
            # validation_datagen = self.validation_data_generator()
            train_generator = self.train_directory_flow(train_datagen)
            validation_generator = self.validation_directory_flow(train_datagen)
            hist = self.train(model, train_generator, validation_generator)
            self.save_graph(hist)
            self.save_history(hist)
            event.set()

    def load_model(self):
        helper = PredictHelper()
        helper.load_model('fruit_iris_core/models/mobilenet.1.h5py')
        return helper.model

    def train_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20,
            validation_split=0.2)

    def validation_data_generator(self):
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
            class_mode='categorical',
            subset='training')

    def validation_directory_flow(self, val_generator):
        return val_generator.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation')

    def train(self, model, train_generator, validation_generator):
        # try to train and save the model
        hist = model.fit_generator(
            generator=train_generator,
            steps_per_epoch=5516 // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator,
            validation_steps=1883 // self.batch_size,
            verbose=True)

        model.save('fruit_iris_core/models/mobilenet.1.h5py')

        return hist

    def save_graph(self, hist):
        accuracy = hist.history['acc']
        val_accuracy = hist.history['val_acc']
        loss = hist.history['loss']
        val_loss = hist.history['val_loss']
        epochs = range(self.epochs)

        plt.figure()
        plt.plot(epochs, accuracy, 'ro', label='Training accuracy')
        plt.plot(epochs, val_accuracy, 'bo', label='Validation accuracy')
        plt.plot(epochs, accuracy, 'r')
        plt.plot(epochs, val_accuracy, 'b')
        plt.title('Training and validation accuracy')
        plt.legend()
        plt.savefig('static/model_history/accuracy.png')

        plt.figure()
        plt.plot(epochs, loss, 'ro', label='Training loss')
        plt.plot(epochs, val_loss, 'bo', label='Validation loss')
        plt.plot(epochs, loss, 'r')
        plt.plot(epochs, val_loss, 'b')
        plt.title('Training and validation loss')
        plt.legend()
        plt.savefig('static/model_history/loss.png')

    def save_history(self, hist):
        with open('static/model_history/history.json', 'w') as f:
            json.dump(hist.history, f)