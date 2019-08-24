import json
import os

from dotmap import DotMap

from apis.utils import url_to_image


def get_photo_type_from_categories(categories):
    top_types = []
    for category in categories:
        name = category['name']
        score = category['score']
        if score > 0.3:
            if 'people_portrait' in name:
                top_types.append(1)
            elif 'people_' in name:
                top_types.append(2)
            elif 'outdoor_' in name or 'building_' in name or 'sky_' in name:
                top_types.append(3)
    if 1 in top_types:
        return 1
    elif 2 in top_types:
        return 2
    elif 3 in top_types:
        return 3
    else:
        return 4


class Photo:
    DATA_FOLDER = ""

    def __init__(self, shortcode, public_url, likes, comments, caption):

        self.filename = None
        self.bboxed_filename = None
        self.shortcode = shortcode
        self.public_url = public_url
        self.instagram_user_id = None

        self.racy_score = 0
        self.adult_score = 0
        self.golden_ratio = 0
        self.description = None

        self.analyze_response = None
        self.face_response = None
        self.emotions_json = None

        self.apparel_response = None

        self.pose_image_filename = None

        self.likes = likes
        self.comments = comments
        self.caption = caption

    @property
    def type(self):
        try:
            categories = json.loads(self.analyze_response)['categories']
            return get_photo_type_from_categories(categories)
        except Exception:
            pass

    @property
    def cv2_image(self):
        return url_to_image(self.public_url)

    @property
    def bboxed_filepath(self):
        if self.bboxed_filename:
            return os.path.join(Photo.DATA_FOLDER, self.bboxed_filename)

    @property
    def emotion(self):
        if self.emotions_json:
            return json.loads(self.emotions_json)
        else:
            return {}

    @property
    def top_emotions(self):
        if self.emotions_json:
            emotion_resp = {}
            emotions = json.loads(self.emotions_json)
            for emotion, value in emotions.items():
                if value > 0.3:
                    emotion_resp[emotion] = value
            return emotion_resp

    @property
    def objects(self):
        if self.analyze_response:
            objects = json.loads(self.analyze_response).get('objects')
            if objects:
                objects = [DotMap(object) for object in objects]
                return objects
            else:
                return {}
        else:
            return {}

    @property
    def engagement(self):
        return self.likes + self.comments

    @property
    def ai_caption(self):
        try:
            return json.loads(self.analyze_response)['description']['captions'][0]['text']
        except:
            pass

    @property
    def pose_image_url(self):
        from flask import url_for
        return url_for('main.data_file', filename=self.pose_image_filename)

    @property
    def apparels(self):
        try:
            return json.loads(self.apparel_response)['articles']
        except:
            pass

    def __repr__(self):
        return "<Photo> {} {}".format(self.type, self.shortcode)
