import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV2Beta
from StringIO import StringIO

def callvisionapi(filename):
    visual_recognition = VisualRecognitionV2Beta(version='2015-12-02', username='0de1dc2a-a669-4894-9577-163f378c7fe9',
                                                 password='t0pyNeJuhW2K')

    # print(json.dumps(visual_recognition.list_classifiers(), indent=2))

    with open(('./static/images/upload/' + filename + '.jpg'), 'rb') as image_file:
        result = visual_recognition.classify(image_file, classifier_ids=["beer_1281902696","waterbottle_298206814","empty_504638325","hand_empty_1903958159","cocacola_1857481479","inside_fridge_937863237","juice_1780138172"])
        return result
