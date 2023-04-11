from flask import Blueprint, render_template

main_blueprint = Blueprint('main_blueprint',
                           __name__,
                           template_folder='templates')


@main_blueprint.route('/')
def page_index():
    return render_template('index.html')


@main_blueprint.route('/choose-hero/')
def page_make_heroes():
    return render_template('hero_choosing.html')


@main_blueprint.route('/fight/')
def page_fight():
    return render_template('fight.html')
