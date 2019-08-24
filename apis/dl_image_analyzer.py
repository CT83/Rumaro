import Algorithmia
import requests

from apis.pose_detection.open_pose_manager import OpenPoseManager
from app.main.deep_learning.models import get_photo_type_from_categories
from app.utils.file_utils import url_to_image


class DlImageAnalyzer:

    def __init__(self, subscription_key, face_subscription_key,
                 public_image_url, deepfashion_api_key=None):
        self.deepfashion_api_key = deepfashion_api_key
        self.subscription_key = subscription_key
        self.face_subscription_key = face_subscription_key
        self.public_image_url = public_image_url

        self.apparel_response = {}

    def analyze_image(self):
        self._basic_analyze()
        if get_photo_type_from_categories(self.analyze_response['categories']) in [1, 2]:
            self._analyze_faces()
            if self.deepfashion_api_key \
                    and get_photo_type_from_categories(self.analyze_response['categories']) in [2]:
                self._analyze_apparel()
            if get_photo_type_from_categories(self.analyze_response['categories']) in [2]:
                self._analyze_pose()
        return self

    def _basic_analyze(self):
        print("Sending image to Vision API...")
        vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
        analyze_url = vision_base_url + "analyze"
        headers = {'Ocp-Apim-Subscription-Key': self.subscription_key}
        params = {'visualFeatures': 'Categories,Description,Color,Brands,Adult,Tags,Faces,Objects',
                  'details': 'Celebrities,Landmarks'}
        data = {'url': self.public_image_url}
        response = requests.post(analyze_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        self.analyze_response = response.json()
        try:
            self.image_caption = analysis["description"]["captions"][0]["text"].capitalize()
        except Exception:
            self.image_caption = ""
        self.racy_score = float(analysis['adult']['racyScore'])
        self.adult_score = float(analysis['adult']['adultScore'])

    def _analyze_faces(self):
        print("Sending image to Face API...")
        face_api_url = 'https://eastus.api.cognitive.microsoft.com/face/v1.0/detect'
        headers = {'Ocp-Apim-Subscription-Key': self.face_subscription_key}
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,'
                                    'accessories,blur,exposure,noise',
        }
        response = requests.post(face_api_url, params=params, headers=headers, json={"url": self.public_image_url})
        analysis = response.json()
        try:
            self.face_response = analysis[0]
            self.emotions_json = analysis[0]['faceAttributes']['emotion']
        except IndexError:
            pass

    def _analyze_apparel(self):
        print("Sending image to DeepFashion")
        input = {
            "image": self.public_image_url,
            "model": "small",
            "threshold": 0.3,
            "tags_only": True
        }
        client = Algorithmia.client(self.deepfashion_api_key)
        algo = client.algo('algorithmiahq/DeepFashion/1.3.0')
        algo.set_options(timeout=300)  # optional
        self.apparel_response = algo.pipe(input).result

    def _analyze_pose(self):
        print("Analysing Pose...")
        pose = OpenPoseManager(cv_image=url_to_image(self.public_image_url))
        self.pose_image = pose.run()
        return self.pose_image
