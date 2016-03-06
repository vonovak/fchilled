import threading
import json

from pusher import Pusher
from models.products import Product
from vision import callvisionapi
from notification import sendNotification

class watsonThread(threading.Thread):
    lastaction = "empty"
    emptycount = 0
    productpicture = ""

    def __init__(self, filename, app):
        threading.Thread.__init__(self)
        self.filename = filename
        self.app = app

    def run(self):
        print "Starting " + self.filename

        tags = callvisionapi(self.filename)

        if("scores" in tags["images"][0]):
            tag = tags["images"][0]["scores"][0]["name"]

            # optimization
            if(tag == "empty" and len(tags["images"][0]["scores"])>1):
                tag = tags["images"][0]["scores"][1]["name"]

            print json.dumps(tags["images"][0]["scores"])

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
                        watsonThread.emptycount = 0

                elif(tag == "inside_fridge" or tag == "hand_empty"):

                    if(watsonThread.lastaction != "empty" and watsonThread.lastaction != "hand_empty" and watsonThread.lastaction != "inside_fridge"):
                        # ADDING PRODUCT INTO FRIDGE

                        with self.app.app_context():
                            prod = Product.query.filter_by(tag=watsonThread.lastaction).first()
                            if(prod != None):
                                prod.add(1)


                        # notify UI
                        sendNotification()
                        notification = {'tag': watsonThread.lastaction, 'filename': watsonThread.productpicture, 'name':'nothing', 'action':'add' }
                        pusher.trigger('messages', 'new_product', notification)

                    watsonThread.lastaction = "inside_fridge"

                else:
                    watsonThread.productpicture = self.filename
                    #PRODUCT
                    if(watsonThread.lastaction == "inside_fridge"):
                        # PRODUCT TAKEN FROM FRIDGE

                        with self.app.app_context():
                            prod = Product.query.filter_by(tag=tag).first()
                            if(prod != None):
                                prod.remove(1)


                        # notify UI
                        sendNotification()
                        notification = {'tag': tag, 'filename': watsonThread.productpicture, 'name':'nothing', 'action':'remove' }
                        pusher.trigger('messages', 'new_product', notification)

                    watsonThread.lastaction = tag



        print "Exiting " + self.filename
