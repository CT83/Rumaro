from flask import render_template, redirect, url_for, send_from_directory, current_app
from flask_login import login_required, current_user
from instaloader import Instaloader, Profile

from app import db
from app.login.views import admin_login_required
from app.main.deep_learning.data_groomer import DataGroomer
from app.main.deep_learning.models import InstagramUser
from app.main.deep_learning.utils import run_analysis, save_bboxed_objs_from_image
from . import main_blueprint


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


@main_blueprint.route('/photo/<filename>')
def view_photo(filename):
    pass


@main_blueprint.route('/confirm-instagram/<instagram_id>', methods=['GET'])
@login_required
def configure_instagram_id(instagram_id):
    current_user.instagram_id = instagram_id
    insta_user = InstagramUser(email=current_user.email, name=current_user.name,
                               instagram_id=current_user.instagram_id)
    db.session.add(insta_user)
    current_user.instagram_user_id = insta_user.id
    db.session.commit()


@main_blueprint.route('/confirm-instagram')
@login_required
def confirm_instagram():
    L = Instaloader()
    profile = Profile.from_username(L.context, current_user.instagram_id)
    return render_template('main/confirm_instagram.html', insta_profile_pic=profile.get_profile_pic_url())


@main_blueprint.route('/setup-payment')
@login_required
def setup_payment():
    return render_template('main/setup_payment.html')


@main_blueprint.route('/start-analysis')
def start_analysis():
    run_analysis(current_user)
    return "Runnning analysis"


@main_blueprint.route('/analyse/<instagram_id>')
def analyse_profile(instagram_id):
    print("Analysing profile as admin...")
    insta_user = InstagramUser.query.filter_by(instagram_id=instagram_id).first() \
                 or InstagramUser(instagram_id=instagram_id)
    db.session.add(insta_user)
    run_analysis(insta_user, notify=False)
    return redirect(url_for('main.view_analysis_admin', insta_user_id=insta_user.id))


@main_blueprint.route('/analysis-started')
def analysis_started():
    run_analysis(current_user)
    return render_template('main/analysis_started.html')


@main_blueprint.route('/analysis')
def view_analysis():
    return "Analysis"


@main_blueprint.route('/temp')
def temp():
    print("Saving bboxed images...")
    for insta_user in InstagramUser.query.all():
        for photo in insta_user.photos:
            photo.bboxed_filename = save_bboxed_objs_from_image(photo)
    db.session.commit()


@main_blueprint.route('/temp-file/<filename>')
def temp_file(filename):
    return send_from_directory(current_app.config['TEMP_FOLDER'], filename=filename)


@main_blueprint.route('/data-file/<filename>')
def data_file(filename):
    return send_from_directory(current_app.config['DATA_FOLDER'], filename=filename)


@main_blueprint.route('/analysis/<insta_user_id>')
def view_analysis_admin(insta_user_id):
    instagram_user = InstagramUser.query.filter_by(id=insta_user_id).first()
    data_groomer = DataGroomer(instagram_user=instagram_user)
    data_groomer.start()
    return render_template('main/analysis_report.html', instagram_user=instagram_user, data_groomer=data_groomer)
