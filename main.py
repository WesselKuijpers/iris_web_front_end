from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
import multiprocessing as mp
from keras import backend as K
import tensorflow as tf
from router import Router
import asyncio
import threading

# this file covers everything that needs to happen only once


# boolean, can be flipped to indicate that the trainingprocesss should start
should_train = True

# if the trainingprocess should commence, configure the trainer and start
if should_train:
    training = Trainer(epochs=2, 
                    batch_size=32, 
                    train_dir='dataset', val_dir='dataset/test', 
                    width=224, height=224)
    event = mp.Event()
    training.start(event)


# start the server
app = Server().start()

# register all the routes/blueprints in the router file
Router().register()


def listen_for_model_change(event):
    while not event.is_set():
        pass
    else:
        app.helper.clear_session()
        app.helper.load_model('fruit_iris_core/models/mobilenet.1.h5py')
        print("MODEL: RELOADED")

x = threading.Thread(target=listen_for_model_change, args=(event,))
x.start()
