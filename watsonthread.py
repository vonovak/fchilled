import threading
import json

from pusher import Pusher
from models.products import Product
from vision import callvisionapi
from notification import sendNotification


class watsonThread(threading.Thread):
    lastaction = ""

    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        print "Starting " + self.filename

        tags = callvisionapi(self.filename)
        tag = {'tag': tags["images"][0]["scores"][0]["name"], 'filename': 'filename'}

        pusher = Pusher(
            app_id='185391',
            key='99c8766f736643bbdfa2',
            secret='68a32b237af4cb110394',
            cluster='eu',
            ssl=True
        )

        print("pushing tag: ")
        print(tag)
        sendNotification()
        pusher.trigger('messages', 'new_product', tag)

        if(tag != watsonThread.lastaction):
            if(tag == "empty"):
                watsonThread.lastaction = ""
            elif(tag == "hand_empty"):
                watsonThread.lastaction = ""
            elif(tag == "inside_fridge"):
                watsonThread.lastaction = "inside_fridge"
            else:
                # PRODUCT
                if(watsonThread.lastaction == "inside_fridge"):
                    # PRODUCT TAKEN FROM FRIDGE
                    prod = Product.query.filter_by(tag=tag).first()
                    prod.remove(1)
                    watsonThread.lastaction = tag


        print "Exiting " + self.filename
