import multiprocessing as mp
import threading

from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
from router import Router

# this file covers everything that needs to happen only once
# the sequence in this file is very important because of keras sessions

# boolean, can be flipped to indicate that the trainingprocesss should start
should_train = False

# if the trainingprocess should commence, configure the trainer and start
if should_train:
    training = Trainer(epochs=100,
                       batch_size=32,
                       train_dir='dataset/train', val_dir='dataset/train', test_dir='dataset/test',
                       width=224, height=224)
    event = mp.Event()
    training.start(event)


# start the server
app = Server().start()

# register all the routes/blueprints in the router file
Router().register()

# asynchronous eventlistener for checking if a training is done and if so reload the model
if should_train:
    def listen_for_model_change(event):
        # while the event is NOT yet set do NOTHING, if it is reload the model
        while not event.is_set():
            pass  # do nothing
        else:
            # clear the keras session
            app.helper.clear_session()
            # reload the model
            app.helper.load_model('fruit_iris_core/models/mobilenet.h5py')
            # let the user know
            print("MODEL: RELOADED")

    # load the eventlistener function into a multithreading thread so that it can be ran asynchronously with the FLASK webserver
    thread = threading.Thread(target=listen_for_model_change, args=(event,))
    thread.start()
