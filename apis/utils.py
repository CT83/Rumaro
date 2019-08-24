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
