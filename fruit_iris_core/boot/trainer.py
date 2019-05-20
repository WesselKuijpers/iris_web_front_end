import json
import multiprocessing as mp

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix

from fruit_iris_core.callbacks.SaveSituations import SaveSituations
from helpers.predict_helper import PredictHelper


# class containing all the methods for starting and maintaining the training process while the FLASK webserver runs
# INT epochs, natural number representing for how many iterations the training process should run
# INT batch_size, natural number representing the size of the batch on which the training should be conducted
# STRING train_dir, path to the directory containing the train data
# STRING val_dir, path to the directory containing the validation data
# STRING test_dir, path to the directory containing the test data
# INT width, natural number representing the pixel width of the training images
# INT height, natural number representing the pixel height of the training images
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

    # method for starting a multiprocessing process for training asynchronously with the FLASK webserver
    # EVENT event, a multiprocessing.event to be passed down and up the chain so that the FLASK webserver gets the signal when the model should be reloaded
    # returns: VOID
    def start(self, event):
        train_process = mp.Process(
            target=self.initialize_trainer, args=(event,))
        train_process.start()

    # method for calling all the methods in the training pipeline
    # EVENT event, a multiprocessing.event to be set when the one training is complete so that the FLASK webserver knows when to reload the model
    # returns: VOID
    def initialize_trainer(self, event):
        # dirty while loop, restarts the training when one has been completed and the metrics have been saved
        while True:
            # configuring the Tensorflow option to consume only a limited amount of GPU memory
            # pass it to keras as the current session
            # this is done to prevent OOM errors
            gpu_options = tf.GPUOptions(
                per_process_gpu_memory_fraction=0.7, allow_growth=True)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
            K.set_session(sess)

            # load the existing model
            model = self.load_model()
            # create a train datagen
            train_datagen = self.train_data_generator()
            # create a train data flow from the train_datagen
            train_generator = self.train_directory_flow(train_datagen)
            # create a validation flow from the train_datagen
            validation_generator = self.validation_directory_flow(
                train_datagen)
            # train the model and asign the history to a variable
            hist = self.train(model, train_generator, validation_generator)

            # create and save graphs for the loss and accuracy
            # self.save_graph(hist)

            # save the history object to a json file
            self.save_history(hist)
            # predict images from a directory flow to be used in generating the classification report and the confusion matrix
            self.predict_test_batch()
            # generate and save a classification report based on the predict_test_batch()
            self.save_classification_report()
            # generate and save a confusion matrix based on the predict_test_batch()
            self.save_confusion_matrix()
            # set the event that was passed in so that the model can be reloaded
            event.set()
            # restart training

    # method for loading the last version of the model so that the training isn't required to start at zero
    # returns: keras.models.Model
    def load_model(self):
        helper = PredictHelper()
        helper.load_model('fruit_iris_core/models/mobilenet.h5py')
        return helper.model

    # method for creating the train ImageDataGenerator
    # returns: keras.preprocessing.image.ImageDataGenerator
    def train_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20,
            validation_split=0.2)

    # method for creating the validation ImageDataGenerator
    # returns: keras.preprocessing.image.ImageDataGenerator
    def validation_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20)

    # method for creating the train ImageDataGenerator.flow_from_directory
    # ImageDataGenerator train_generator, a train data generator
    # returns: keras.preprocessing.image.ImageDataGenerator.flow_from_directory
    def train_directory_flow(self, train_generator):
        return train_generator.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='training')

    # method for creating the validation ImageDataGenerator.flow_from_directory
    # ImageDataGenerator val_generator, a validation data generator
    # returns: keras.preprocessing.image.ImageDataGenerator.flow_from_directory
    def validation_directory_flow(self, val_generator):
        return val_generator.flow_from_directory(
            self.train_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical',
            subset='validation')

    # method for creating the test ImageDataGenerator
    # returns: keras.preprocessing.image.ImageDataGenerator
    def test_data_generator(self):
        return ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=20)

    # method for creating the test ImageDataGenerator.flow_from_directory
    # ImageDataGenerator test_generator, a test data generator
    # returns: keras.preprocessing.image.ImageDataGenerator.flow_from_directory
    def test_directory_flow(self, test_generator):
        return test_generator.flow_from_directory(
            self.test_dir,
            target_size=(self.width, self.height),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

    # method for the actual training or 'fit' of the data to the model
    # keras.models.Model model, the model that was loaded from disk
    # ImageDataGenerator train_generator, a directory flow for the train data
    # ImageDataGenerator validation_generator, a directory flow for the validation data
    # returns: DICT
    def train(self, model, train_generator, validation_generator):
        # callbacks
        checkpoint = ModelCheckpoint('fruit_iris_core/models/mobilenet.h5py', monitor='val_acc',
                                     verbose=1, save_best_only=False, mode='max', save_weights_only=False)
        save_situations = SaveSituations(epochs=self.epochs)

        # try to train and save the model
        hist = model.fit_generator(
            generator=train_generator,
            steps_per_epoch=5516 // self.batch_size,
            epochs=self.epochs,
            validation_data=validation_generator,
            validation_steps=1883 // self.batch_size,
            verbose=True,
            callbacks=[checkpoint, save_situations])

        return hist

    # DEPRECATED
    # method for saving images of the loss and accuracy graphs
    # DICT hist, a dict containing information about the last training process
    # returns: VOID
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

    # method for predicting classes for a batch of images, this is used for the classification report and the confusion matrix
    # returns: VOID
    def predict_test_batch(self):
        model = self.load_model()
        test_datagen = self.test_data_generator()
        test_dir_flow = self.test_directory_flow(test_datagen)
        y_pred = model.predict_generator(test_dir_flow, 324)
        y_pred = np.argmax(y_pred, axis=1)

        self.y_pred = y_pred
        self.test_flow = test_dir_flow

    # method for saving the history object to a json file
    # DICT hist, a dict containing information about the last training process
    # returns: VOID
    def save_history(self, hist):
        with open('static/model_history/history.json', 'w') as f:
            json.dump(hist.history, f)

    # method for generating and saving a classification report
    # returns: VOID
    def save_classification_report(self):
        with open('fruit_iris_core/classes.json', 'r') as file:
            classes = json.load(file)

        cr = classification_report(
            self.test_flow.classes, self.y_pred, target_names=classes, output_dict=True)

        with open('static/model_history/classification_report.json', 'w') as file:
            json.dump(cr, file)

    # method for generating and saving a confusion matrix
    # returns: VOID
    def save_confusion_matrix(self):
        cm = confusion_matrix(self.test_flow.classes, self.y_pred)

        with open('static/model_history/confusion_matrix.json', 'w') as file:
            json.dump(cm.tolist(), file)
