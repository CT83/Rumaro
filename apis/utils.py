import os


def url_to_image(url):
    """Converts url to cv2 image"""
    import numpy as np
    import cv2
    from six.moves.urllib.request import urlopen

    try:
        resp = urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        from flask import current_app
        print(e)
        current_app.logger.error(str(e))


def create_dir_if_not_exists(output_dir):
    try:
        os.makedirs(output_dir)
        return output_dir
    except OSError:
        if not os.path.isdir(output_dir):
            raise OSError("Failed to create" + output_dir)


def print_report(data_groomer, instagram_user):
    print(instagram_user.name, "-", instagram_user.instagram_id)
    print("Profile Picture", instagram_user.profile_picture_url)

    print("Followers:", instagram_user.followers)
    print("Engagement Rate", data_groomer.engagement_rate)

    print("What does your post distribution look like?")
    print("Total Number of Photos: ", len(instagram_user.photos))
    print("Portraits: ", len(data_groomer.portrait_photos))
    print("Pose Photos: ", len(data_groomer.social_photos))
    print("Scenery: ", len(data_groomer.scenery_photos))
    print("Other Photos: ", len(data_groomer.other_photos))

    print("Emotions")
    print("Emotional Distribution", data_groomer.emotions_distribution_chart())
    print("Emotions V/s Engagement", data_groomer.emotion_vs_enagagement_chart())
    print("Photo Type V/s Engagement", data_groomer.photo_type_vs_enagagement_chart())
    print("Does racy-ness drive engagement", data_groomer.racy_vs_engagement_chart())
