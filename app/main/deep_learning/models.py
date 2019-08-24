import json
import os

from dotmap import DotMap
from flask import current_app

from app.utils.file_utils import url_to_image

IMAGE_TYPES = {
    1: 'selfie',
    2: 'people',
    3: 'scenery',
    4: 'unclassified'
}

from app import db


class InstagramUser(db.Model):
    __tablename__ = 'instagram_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    name = db.Column(db.Text)

    analyzed = db.Column(db.Boolean, default=False)
    instagram_id = db.Column(db.String(100))
    photos = db.relationship("Photo", backref='instagram_user', lazy=True)
    attractiveness = db.Column(db.Float)
    engagement_rate = db.Column(db.Float)
    followers = db.Column(db.Integer())
    profile_picture_url = db.Column(db.String())


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


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    bboxed_filename = db.Column(db.String)
    shortcode = db.Column(db.String)
    public_url = db.Column(db.String)
    instagram_user_id = db.Column(db.Integer, db.ForeignKey('instagram_user.id'), nullable=True)

    racy_score = db.Column(db.Float)
    adult_score = db.Column(db.Float)
    golden_ratio = db.Column(db.Float)
    description = db.Column(db.String)

    analyze_response = db.Column(db.String)  # Stores the actual response from Cognitive Services Analyze API
    face_response = db.Column(db.String)  # Stores the actual response from Cognitive Services Face API
    emotions_json = db.Column(db.String)

    apparel_response = db.Column(db.String)

    pose_image_filename = db.Column(db.String)

    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    caption = db.Column(db.Text)

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
            return os.path.join(current_app.config['DATA_FOLDER'], self.bboxed_filename)

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
