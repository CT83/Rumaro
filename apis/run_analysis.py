import json
import os
import time
import uuid
from itertools import islice

import cv2
from instaloader import Profile, Instaloader

from apis.config import DATA_FOLDER, MAX_POSTS_TO_ANALYSE, DEEPFASHION_API_KEY, IMAGE_TYPES
from apis.data_groomer import DataGroomer
from apis.dl_image_analyzer import DlImageAnalyzer
from apis.photo import Photo
from app.utils.file_utils import draw_bbox_on_image


def run_analysis(instagram_id):
    L = Instaloader()
    profile = Profile.from_username(L.context, instagram_id)
    posts = profile.get_posts()

    if profile.mediacount > MAX_POSTS_TO_ANALYSE:
        posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda p: p.likes + p.comments)
        posts = []
        for post in islice(posts_sorted_by_likes, MAX_POSTS_TO_ANALYSE):
            posts.append(post)

    instagram_user.name = profile.full_name
    instagram_user.followers = profile.followers
    instagram_user.profile_picture_url = profile.get_profile_pic_url()

    photos = []
    for post in posts:
        photo = Photo(shortcode=post.shortcode, public_url=post.url,
                      likes=post.likes, comments=post.comments, caption=post.caption)
        photos.append(photo)

    print("Total Photos {} by {}".format(len(photos), instagram_id))
    for photo in photos:
        print("Analysing {} of {}...".format(photos.index(photo), len(photos)))

        analyzer = DlImageAnalyzer(subscription_key=os.environ['MS_COGNITIVE_VISION_KEY'],
                                   face_subscription_key=os.environ['MS_COGNITIVE_FACE_KEY'],
                                   public_image_url=photo.public_url,
                                   deepfashion_api_key=DEEPFASHION_API_KEY)
        analyzer.analyze_image()
        photo.description = analyzer.image_caption
        photo.racy_score = analyzer.racy_score
        photo.adult_score = analyzer.adult_score
        photo.analyze_response = json.dumps(analyzer.analyze_response)
        photo.apparel_response = json.dumps(analyzer.apparel_response)

        if IMAGE_TYPES[photo.type] in ['selfie', 'people']:
            try:
                photo.face_response = json.dumps(analyzer.face_response)
                photo.emotions_json = json.dumps(analyzer.emotions_json)
            except AttributeError:
                pass
        try:
            filename = str(uuid.uuid1()) + '.jpg'
            cv2.imwrite(os.path.join(DATA_FOLDER, filename), analyzer.pose_image)
            photo.pose_image_filename = filename
        except:
            pass

        photo.bboxed_filename = save_bboxed_objs_from_image(photo)
        time.sleep(4)


    data_groomer = DataGroomer(instagram_user=instagram_user)
    data_groomer.start()
    print("Analyzed {}'s Profile Sucessfully!".format(instagram_id))


def save_bboxed_objs_from_image(photo):
    print("Saving bboxed images...")
    image = photo.cv2_image
    for obj in photo.objects:
        image = draw_bbox_on_image(image, obj.rectangle.x, obj.rectangle.y,
                                   obj.rectangle.x + obj.rectangle.w,
                                   obj.rectangle.y + obj.rectangle.h,
                                   obj.object + " " + str(obj.confidence),
                                   color=(0, 255, 0),
                                   thickness=3)
    f_name = str(uuid.uuid1()) + '.jpg'
    cv2.imwrite(os.path.join(DATA_FOLDER, f_name), image)
    return f_name
