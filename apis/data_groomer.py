import os
import uuid

import matplotlib.pyplot as plt

from apis.config import IMAGE_TYPES, TEMP_FOLDER


class DataGroomer:

    def __init__(self, instagram_user):
        self.instagram_user = instagram_user

        self.portrait_photos = self.sort_photos('selfie')
        self.social_photos = self.sort_photos('people')
        self.scenery_photos = self.sort_photos('scenery')
        self.other_photos = self.sort_photos('unclassified')
        self.all_photos = self.sort_photos()

        self.most_liked_post = None
        self.most_commented_post = None
        self.most_liked_emotion = None

    def start(self):
        self.racy_vs_engagement_chart()

    def sort_photos(self, photo_type=None):
        if photo_type:
            photos = [photo for photo in self.instagram_user.photos if IMAGE_TYPES.get(photo.type) == photo_type]
        else:
            photos = self.instagram_user.photos
        photos.sort(key=lambda x: x.likes + x.comments, reverse=True)
        return photos

    @property
    def total_likes(self):
        total_likes = 0
        for photo in self.instagram_user.photos:
            try:
                total_likes += int(photo.likes)
            except AttributeError:
                pass
        return total_likes

    @property
    def total_comments(self):
        comments = 0
        for photo in self.instagram_user.photos:
            try:
                comments += int(photo.comments)
            except AttributeError:
                pass
        return comments

    @property
    def engagement_rate(self):
        rate = (self.total_likes + self.total_comments) / (self.instagram_user.followers * 100)
        return round(rate, 2)

    def count_likes(self, photos):
        total_likes = 0
        for photo in photos:
            try:
                total_likes += int(photo.likes)
            except AttributeError:
                pass
        return total_likes

    def count_comments(self, photos):
        total_comments = 0
        for photo in photos:
            try:
                total_comments += int(photo.comments)
            except AttributeError:
                pass
        return total_comments

    def frequency_emotions(self, photos):
        freq_emotion = {}
        for photo in photos:
            if photo.emotion:
                for emotion_value in photo.emotion.values():
                    if emotion_value > 0.4:
                        t = [emotion for emotion, value in photo.emotion.items() if value == emotion_value]
                        emotion = freq_emotion.get(t[0], 0)
                        emotion += 1
                        freq_emotion[t[0]] = emotion
        return freq_emotion

    def get_racy_vs_enagement_scores(self):
        photos = self.social_photos
        photos.sort(key=lambda x: x.racy_score, reverse=False)
        racy_scores = []
        engagements = []

        for photo in photos:
            racy_scores.append(photo.racy_score)
            engagements.append(photo.likes)
        return racy_scores, engagements

    def racy_vs_engagement_chart(self):
        racy_scores, engagements = self.get_racy_vs_enagement_scores()
        plt.plot(racy_scores, engagements)
        filename = self.save_plot_to_file()
        return filename

    def emotions_distribution_chart(self):
        dictionary = self.frequency_emotions(self.all_photos)
        plt.bar(range(len(dictionary)), list(dictionary.values()), align='center')
        plt.xticks(range(len(dictionary)), list(dictionary.keys()))
        filename = self.save_plot_to_file()
        return filename

    def emotion_vs_enagagement_chart(self):
        emotion_engagement = {}
        for photo in self.all_photos:
            if photo.top_emotions:
                for emotion, value in photo.top_emotions.items():
                    emotion_engagement[emotion] = emotion_engagement.get(emotion, 0) + photo.engagement
        plt.bar(range(len(emotion_engagement)), list(emotion_engagement.values()), align='center')
        plt.xticks(range(len(emotion_engagement)), list(emotion_engagement.keys()))
        filename = self.save_plot_to_file()
        return filename

    def photo_type_vs_enagagement_chart(self):
        photo_type_engage = {
            'portrait': self.count_likes(self.portrait_photos) + self.count_comments(self.portrait_photos),
            'pose': self.count_likes(self.social_photos) + self.count_comments(self.social_photos),
            'outdoor': self.count_likes(self.scenery_photos) + self.count_comments(self.scenery_photos),
            'other': self.count_likes(self.other_photos) + self.count_comments(self.other_photos),
        }

        plt.bar(range(len(photo_type_engage)), list(photo_type_engage.values()), align='center')
        plt.xticks(range(len(photo_type_engage)), list(photo_type_engage.keys()))
        filename = self.save_plot_to_file()
        return filename

    def save_plot_to_file(self):
        filename = str(uuid.uuid1()) + '.png'
        plt.savefig(os.path.join(TEMP_FOLDER, filename), bbox_inches='tight')
        plt.close()
        return filename

    @property
    def top_pose_images(self):
        res = []
        for photo in self.social_photos[:25]:
            if photo.pose_image_filename:
                res.append(photo)
        return res
