from keras.callbacks import Callback
import json

class SaveSituation(Callback):
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

        with open('static/model_history/situation.json', 'r') as file:
            situation = json.load(file)

        situation['previous_situation'] = situation['current_situation']
        situation['current_situation'] = current_situation

        with open('static/model_history/situation.json', 'w') as file:
            json.dump(situation, file)

