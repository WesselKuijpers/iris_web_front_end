from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
import multiprocessing as mp
from keras import backend as K
import tensorflow as tf
from router import Router

# this file covers everything that needs to happen only once

# start the server
app = Server().start()

# boolean, can be flipped to indicate that the trainingprocesss should start
should_train = False

# if the trainingprocess should commence, configure the trainer and start
if should_train:
    training = Trainer(epochs=5, 
                    batch_size=32, 
                    train_dir='dataset/train', val_dir='dataset/test', 
                    width=224, height=224)
    training.start()


# register all the routes/blueprints in the router file
Router().register()
