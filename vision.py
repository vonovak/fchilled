import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV2Beta


def callvisionapi(filename):
    visual_recognition = VisualRecognitionV2Beta(version='2015-12-02', username='0de1dc2a-a669-4894-9577-163f378c7fe9',
                                                 password='t0pyNeJuhW2K')

    # print(json.dumps(visual_recognition.list_classifiers(), indent=2))

    with open(('./uploads/' + filename + '.jpg'), 'rb') as image_file:
        result = (json.dumps(visual_recognition.classify(image_file, classifier_ids=[]), indent=2))
        print result
        return result
