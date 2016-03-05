import threading
from vision import callvisionapi


class watsonThread(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        print "Starting " + self.filename

        watson = callvisionapi(self.filename)

        print "Exiting " + self.filename
