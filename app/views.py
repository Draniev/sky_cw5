from flask import Blueprint, render_template

main_blueprint = Blueprint('main_blueprint',
                           __name__,
                           template_folder='templates')


@main_blueprint.route('/')
def page_index():
    return render_template('index.html')
