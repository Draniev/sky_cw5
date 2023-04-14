from flask import Blueprint, jsonify, render_template, request

from arena.equipment import Armor, Weapon

from .container import armor_service, unit_factory, weapon_service, arena
from .utils import names_list

main_blueprint = Blueprint('main_blueprint',
                           __name__,
                           template_folder='templates')


@main_blueprint.route('/')
def page_index():
    return render_template('index.html')


@main_blueprint.route('/choose-hero/', methods=['GET'])
@main_blueprint.route('/choose-enemy/', methods=['GET'])
def page_choose_heroes():
    armors = armor_service.get_all()
    weapons = weapon_service.get_all()
    armor_names = names_list(armors)
    weapon_names = names_list(weapons)

    if request.path == '/choose-hero/':
        header = "Выберите характеристики своего героя"
    else:
        header = "Выберите характеристики соперника"

    result = {'header': header,
              'classes': ['warrior', 'thief', 'priest'],
              'armors': armor_names,
              'weapons': weapon_names
              }
    return render_template('hero_choosing.html', result=result)


@main_blueprint.route('/choose-hero/', methods=['POST'])
@main_blueprint.route('/choose-enemy/', methods=['POST'])
def page_make_heroes():
    unit_data = request.form
    weapon = weapon_service.get_by_name(unit_data['weapon'])
    armor = armor_service.get_by_name(unit_data['armor'])
    unit = unit_factory.create(unit_data['name'],
                               unit_data['unit_class'],
                               Weapon.from_orm(weapon),
                               Armor.from_orm(armor)
                               )
    return f"{weapon.name} {armor.name} {unit}"


@main_blueprint.route('/fight/')
def page_fight():
    # return render_template('fight.html')
    return "Тут будет бой персонажей"
