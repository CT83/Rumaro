import os

import cv2
from numpy import unicode


def resolve_image_path_as_url(image_path, root_dir='media/predictions/'):
    try:
        filename = os.path.basename(image_path)
    except Exception as e:
        filename = ""
        print(image_path)
        print(e)
    from flask import url_for
    return url_for('static', filename=root_dir + filename)


def delete_flask_sessions(sessions_path="flask_sessions"):
    import shutil
    try:
        shutil.rmtree(sessions_path)
    except:
        pass


def cleanup():
    delete_flask_sessions()


def add_sources_to_path():
    """Useful to run scripts outside Pycharm"""
    import os
    import sys

    sources_path = os.path.realpath(__file__)
    sources_folder = "Shepherd"
    sources_path = sources_path[:sources_path.find(sources_folder) + len(sources_folder)]
    sys.path.append(sources_path)
    print(sys.path)


def create_uploads_folder(uploads_subdir):
    import os
    if not os.path.exists(uploads_subdir):
        os.makedirs(uploads_subdir)


def create_dir_if_not_exists(output_dir):
    try:
        os.makedirs(output_dir)
        return output_dir
    except OSError:
        if not os.path.isdir(output_dir):
            raise OSError("Failed to create" + output_dir)


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


def is_path_video(path, supported_video_extensions=('.mp4', '.MP4')):
    extension = os.path.splitext(os.path.basename(path))[1]
    if extension in supported_video_extensions:
        return True
    else:
        return False


def draw_bbox_on_image(frame, x1, y1, x2, y2, text, color=(0, 0, 0), thickness=3):
    if type(color) in (str, unicode):
        color = color.lstrip('#')
        rgb = (color[:2], color[2:4], color[4:])
        color = tuple(int(x, 16) for x in rgb)
    cv2.rectangle(frame, (x1, y1), (x2, y2),
                  color=color, thickness=thickness)
    cv2.putText(frame, text, (x1, y1),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)
    return frame
