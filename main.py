from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
import multiprocessing as mp
from keras import backend as K
import tensorflow as tf

# this file covers everything that needs to happen only once


# configuring the Tensorflow option to consume only a limited amount of GPU memory
# pass it to keras as the current session
# this is done to prevent OOM errors
gpu_options = tf.GPUOptions(
    per_process_gpu_memory_fraction=0.8, allow_growth=True)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
K.set_session(sess)

# start the server
app = Server().start()

# boolean, can be flipped to indicate that the trainingprocesss should start
should_train = False

# if the trainingprocess should commence, configure the trainer and start
if should_train:
    train = Trainer(epochs=5, 
                    batch_size=32, 
                    train_dir='dataset/train', val_dir='dataset/test', 
                    width=224, height=224)
    train.start()
