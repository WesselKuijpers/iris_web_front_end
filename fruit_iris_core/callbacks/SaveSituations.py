import json

from keras.callbacks import Callback

# a class containing a method specifying a custom callback on epoch end saving the current situation to a file
# extends: keras.callbacks.Callback
# INT epochs, a natural number indicating for how much iterations the training will be runnning
# returns: VOID
class SaveSituations(Callback):
    def __init__(self, epochs):
        self.epochs = epochs

    # method that defines a callback on epoch end to save the current situation
    # INT epoch, a natural number representing the current iteration of the training (required by extension)
    # <UNKNOWN> logs, log of the current training iteration (required by extension)
    # returns: VOID
    def on_epoch_end(self, epoch, logs={}):
        cepoch = epoch + 1
        current_situation = {}
        current_situation['epochs'] = self.epochs
        current_situation['epoch'] = cepoch
        current_situation['acc'] = logs.get('acc')
        current_situation['val_loss'] = logs.get('val_loss')
        current_situation['val_acc'] = logs.get('val_acc')
        current_situation['loss'] = logs.get('loss')

        situation = None

        with open('static/model_history/situations.json', 'r') as file:
            situations = json.load(file)

        new_situations = [current_situation]

        if (epoch != 0):
            for situation in situations:
                new_situations.append(situation)

        with open('static/model_history/situations.json', 'w') as file:
            json.dump(new_situations, file)
