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
from sklearn.metrics import classification_report, confusion_matrix
from keras.callbacks import ModelCheckpoint, RemoteMonitor



# TODO: More SOLID
class Trainer:
    def __init__(self, epochs, batch_size, train_dir, val_dir, test_dir, width, height):
        self.epochs = epochs
        self.batch_size = batch_size
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.test_dir = test_dir
        self.width = width
        self.height = height
        self.model = None
        self.y_pred = None
        self.test_flow = None

    def start(self, event):
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
            self.predict_test_batch()
            self.save_classification_report()
            self.save_confusion_matrix()
            event.set()

    def load_model(self):
        helper = PredictHelper()
        helper.load_model('fruit_iris_core/models/mobilenet.3.h5py')
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

    def test_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20)

    def test_directory_flow(self, test_generator):
        return test_generator.flow_from_directory(
            self.test_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

    def train(self, model, train_generator, validation_generator):

        checkpoint = ModelCheckpoint('fruit_iris_core/models/mobilenet.3.h5py', monitor='val_acc', verbose=1, save_best_only=False, mode='max', save_weights_only=False)
        remote = RemoteMonitor(root='http://localhost:5000', path='/insight/stream/catch', headers={'epochs': str(self.epochs)}, field='data', send_as_json=False)
        # try to train and save the model
        hist = model.fit_generator(
            generator=train_generator,
            steps_per_epoch=5516 // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator,
            validation_steps=1883 // self.batch_size,
            verbose=True,
            callbacks=[checkpoint, remote])

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

    def predict_test_batch(self):
        model = self.load_model()
        test_datagen = self.test_data_generator()
        test_dir_flow = self.test_directory_flow(test_datagen)
        y_pred = model.predict_generator(test_dir_flow, 324)
        y_pred = np.argmax(y_pred, axis=1)

        self.y_pred = y_pred
        self.test_flow = test_dir_flow


    def save_history(self, hist):
        with open('static/model_history/history.json', 'w') as f:
            json.dump(hist.history, f)

    def save_classification_report(self):
        with open('fruit_iris_core/classes.json', 'r') as file:
            classes = json.load(file)

        cr = classification_report(self.test_flow.classes, self.y_pred, target_names=classes, output_dict=True)

        with open('static/model_history/classification_report.json', 'w') as file:
            json.dump(cr, file)

    def save_confusion_matrix(self):
        cm = confusion_matrix(self.test_flow.classes, self.y_pred)

        with open('static/model_history/confusion_matrix.json', 'w') as file:
            json.dump(cm.tolist(), file)
            