from keras.callbacks import Callback
import json

class SaveSituations(Callback):
    def __init__(self, epochs):
        self.epochs = epochs

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
