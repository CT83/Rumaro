from app.main.deep_learning.data_groomer import DataGroomer
from app.main.deep_learning.models import InstagramUser


def run_analysis(insta_user_id):
    instagram_user = InstagramUser.query.filter_by(id=insta_user_id).first()
    data_groomer = DataGroomer(instagram_user=instagram_user)
    data_groomer.start()
    print(data_groomer)


if __name__ == '__main__':
    run_analysis()