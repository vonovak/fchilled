import threading
import json

from pusher import Pusher
from models.products import Product
from vision import callvisionapi
from notification import sendNotification


class watsonThread(threading.Thread):
    lastaction = ""
    emptycount = 0

    def __init__(self, filename, app):
        threading.Thread.__init__(self)
        self.filename = filename
        self.app = app

    def run(self):
        print "Starting " + self.filename

        tags = callvisionapi(self.filename)

        if("scores" in tags["images"][0]):
            tag = tags["images"][0]["scores"][0]["name"]


            pusher = Pusher(
                app_id='185391',
                key='99c8766f736643bbdfa2',
                secret='68a32b237af4cb110394',
                cluster='eu',
                ssl=True
            )

            print("received tag: ")
            print(tag)

            if(tag != watsonThread.lastaction):
                if(tag == "empty"):

                    # do nothing
                    watsonThread.emptycount += 1
                    # TO MAKE SURE THE EMPTY TAG WASNT MISRECOGNIZED
                    if(watsonThread.emptycount > 1):
                        watsonThread.lastaction = ""

                elif(tag == "inside_fridge" or tag == "hand_empty"):

                    if(watsonThread.lastaction != "empty" and watsonThread.lastaction != "hand_empty"):
                        # ADDING PRODUCT INTO FRIDGE

                        with self.app.app_context():
                            prod = Product.query.filter_by(tag=watsonThread.lastaction).first()
                            prod.add(1)


                        # notify UI
                        sendNotification()
                        notification = {'tag': watsonThread.lastaction, 'filename': self.filename, 'name':'nothing' }
                        pusher.trigger('messages', 'new_product', notification)

                    watsonThread.lastaction = "inside_fridge"

                else:

                    # PRODUCT
                    if(watsonThread.lastaction == "inside_fridge"):
                        # PRODUCT TAKEN FROM FRIDGE

                        with self.app.app_context():
                            prod = Product.query.filter_by(tag=tag).first()
                            prod.remove(1)


                        # notify UI
                        sendNotification()
                        notification = {'tag': tag, 'filename': self.filename, 'name':'nothing' }
                        pusher.trigger('messages', 'new_product', notification)

                    watsonThread.lastaction = tag



        print "Exiting " + self.filename
