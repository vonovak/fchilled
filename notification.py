from gcm import GCM


def sendNotification():
    gcm = GCM('AIzaSyClrjv8zPzVAq68NG3zCZxotNmmD6GQO3I')
    data = {'key': 'value'}

    # Downstream message using JSON request
    # reg_ids = ['fchQE_Fhj58:APA91bFvFKCt9Hce1se9CqFvZ92v2xf51MYjKA6ZWFHxa1KYAQ7M2BoE5tgiPo265uzwibsuvSkFKSRXgzN2Ivz7roFOlFaiGDw9qI98TkgXLXbSRJES2iaxul-QxxyfApfC7iBMB2UV']
    # response = gcm.json_request(registration_ids=reg_ids, data=data)

    registration_id = 'fchQE_Fhj58:APA91bFvFKCt9Hce1se9CqFvZ92v2xf51MYjKA6ZWFHxa1KYAQ7M2BoE5tgiPo265uzwibsuvSkFKSRXgzN2Ivz7roFOlFaiGDw9qI98TkgXLXbSRJES2iaxul-QxxyfApfC7iBMB2UV'

    data = {'param1': 'value1', 'param2': 'value2'}

    response = gcm.plaintext_request(registration_id=registration_id, data=data)

    print(response)
