from fruit_iris_core.boot.server import Server
from fruit_iris_core.boot.trainer import Trainer
import multiprocessing as mp

train = Trainer(epochs=5, batch_size=32, train_dir='dataset/train', val_dir='dataset/test', width=224, height=224)

# server_process = mp.Process(target=server.start)
# train_process = mp.Process(target=train.start)

app = Server().start()
train.start()