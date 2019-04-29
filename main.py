from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
import multiprocessing as mp
from keras import backend as K
import tensorflow as tf

# this file covers everything that needs to happen only once

# boolean, can be flipped to indicate that the trainingprocesss should start
should_train = True

# if the trainingprocess should commence, configure the trainer and start
# if should_train:
training = Trainer(epochs=5, 
                batch_size=32, 
                train_dir='dataset', val_dir='dataset/test', 
                width=224, height=224)
training.start()

# start the server
app = Server().start()
