import multiprocessing as mp
import threading

from iris_core.boot.server import Server
from router import Router

# this file covers everything that needs to happen only once, when the app starts
# the sequence in this file is very important because of keras sessions

# start the server
app = Server().start()

# register all the routes/blueprints in the router file
Router().register()
