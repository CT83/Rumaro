import json
import os
import time
import uuid
from itertools import islice

import cv2
from flask import current_app
from instaloader import Profile, Instaloader
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app import db
from app.main.deep_learning.dl_image_analyzer import DlImageAnalyzer
from app.main.deep_learning.instagram_dm.InstagramAPI import InstagramAPI
from app.main.deep_learning.models import Photo, IMAGE_TYPES
from app.utils.file_utils import draw_bbox_on_image


def run_analysis(instagram_user, notify=True):
    current_app.logger.info("Starting analysis on {}...".format(instagram_user.instagram_id))
    L = Instaloader()
    profile = Profile.from_username(L.context, instagram_user.instagram_id)
    posts = profile.get_posts()

    if profile.mediacount > current_app.config['MAX_POSTS_TO_ANALYSE']:
        posts_sorted_by_likes = sorted(profile.get_posts(), key=lambda p: p.likes + p.comments)
        posts = []
        for post in islice(posts_sorted_by_likes, current_app.config['MAX_POSTS_TO_ANALYSE']):
            posts.append(post)

    instagram_user.name = profile.full_name
    instagram_user.followers = profile.followers
    instagram_user.profile_picture_url = profile.get_profile_pic_url()

    # Delete existing
    for photo in instagram_user.photos:
        db.session.delete(photo)

    db.session.commit()

    for post in posts:
        photo = Photo(shortcode=post.shortcode, public_url=post.url, instagram_user_id=instagram_user.id,
                      likes=post.likes, comments=post.comments, caption=post.caption)
        db.session.add(photo)
    db.session.commit()

    current_app.logger.info("Total Photos {} by {}".format(len(instagram_user.photos), instagram_user.instagram_id))
    for photo in instagram_user.photos:
        current_app.logger.info(
            "Analysing {} of {}...".format(instagram_user.photos.index(photo), len(instagram_user.photos)))
        if current_app.config['ENABLE_DEEP_FASHION']:
            analyzer = DlImageAnalyzer(subscription_key=os.environ['MS_COGNITIVE_VISION_KEY'],
                                       face_subscription_key=os.environ['MS_COGNITIVE_FACE_KEY'],
                                       public_image_url=photo.public_url,
                                       deepfashion_api_key=current_app.config['DEEPFASHION_API_KEY'])
        else:
            analyzer = DlImageAnalyzer(subscription_key=os.environ['MS_COGNITIVE_VISION_KEY'],
                                       face_subscription_key=os.environ['MS_COGNITIVE_FACE_KEY'],
                                       public_image_url=photo.public_url, )
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
            cv2.imwrite(os.path.join(current_app.config['DATA_FOLDER'], filename), analyzer.pose_image)
            photo.pose_image_filename = filename
        except:
            pass

        photo.bboxed_filename = save_bboxed_objs_from_image(photo)
        db.session.commit()

        time.sleep(4)
    instagram_user.analyzed = True
    db.session.commit()
    current_app.logger.info("Analyzed {}'s Profile Sucessfully!".format(instagram_user.instagram_id))

    if notify:
        notify_user(instagram_user)


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
    cv2.imwrite(os.path.join(current_app.config['DATA_FOLDER'], f_name), image)
    return f_name


def notify_user(user):
    link = ""
    subject = "Results are in - Profile Analysis Completed!"
    message = "Our AI has completed analysing your profile, " \
              "Visit {} to view them.".format(link)

    current_app.logger.info("Notfying {} via DM ".format(user.instagram_id))
    api = InstagramAPI(current_app.config['INSTAGRAM_USERNAME'], current_app.config['INSTAGRAM_PASSWORD'])
    api.login()
    time.sleep(2)
    # api.searchUsername(user.instagram_id)
    api.searchUsername('betadesignercom')  # example 'cassianokunsch'
    response = api.LastJson
    user_id = response['user']['pk']
    api.direct_message(subject + "\n" + message, user_id)

    current_app.logger.info("Notfying {} via Email ".format(user.instagram_id))
    message = Mail(
        from_email=current_app.config['SENDGRID_EMAIL'],
        to_emails=user.email,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


if __name__ == '__main__':
    # notify_user(None)
    DlImageAnalyzer(subscription_key=os.environ['MS_COGNITIVE_VISION_KEY'],
                    face_subscription_key=os.environ['MS_COGNITIVE_FACE_KEY'],
                    public_image_url="https://instagram.fbom16-1.fna.fbcdn.net/vp/80544ba9c3ca6aff0f7f01c493037bdb/5D8405FB/t51.2885-19/s320x320/57648989_2246160068978357_3472571274604052480_n.jpg?_nc_ht=instagram.fbom16-1.fna.fbcdn.net").analyze_image()
