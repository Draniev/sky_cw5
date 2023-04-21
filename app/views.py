from flask import Blueprint, render_template, request, redirect

from arena.equipment import Armor, Weapon

from .container import armor_service, unit_factory, weapon_service, arena, hall_of_fame_service
from .utils import names_list
from .npc_logic import npc_choose_action

main_blueprint = Blueprint('main_blueprint',
                           __name__,
                           template_folder='templates')


@main_blueprint.route('/')
def page_index():
    arena.get_clean()
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
    if request.path == '/choose-hero/':
        arena.set_unit('hero', unit)
        return redirect(location='/choose-enemy/')
    else:
        arena.set_unit('enemy', unit)
        arena.start()
        return redirect(location='/fight/')


@main_blueprint.route('/fight/', methods=['GET'])
def page_fight():
    battle_log = arena.log.get_plain_log()
    return render_template('fight.html', arena=arena, battle_log=battle_log)


@main_blueprint.route('/fight/hit/', methods=['GET'])
def page_fight_hit():
    arena.set_action('hero', 'hit')
    enemy_action = npc_choose_action(arena._units['enemy'])
    arena.set_action('enemy', enemy_action)
    arena.fight_cur_round()
    return redirect(location='/fight/')


@main_blueprint.route('/fight/use-skill/', methods=['GET'])
def page_fight_use_skill():
    arena.set_action('hero', 'feat')
    enemy_action = npc_choose_action(arena._units['enemy'])
    arena.set_action('enemy', enemy_action)
    arena.fight_cur_round()
    return redirect(location='/fight/')


@main_blueprint.route('/fight/pass-turn/', methods=['GET'])
def page_fight_pass_turn():
    arena.set_action('hero', 'pass')
    enemy_action = npc_choose_action(arena._units['enemy'])
    arena.set_action('enemy', enemy_action)
    arena.fight_cur_round()
    return redirect(location='/fight/')


@main_blueprint.route('/fight/end-fight/', methods=['GET'])
def page_fight_end_fight():
    arena.force_stop()
    arena.fight_cur_round()
    return redirect(location='/fight/')


@main_blueprint.route('/save-results/', methods=['GET'])
def page_save_results():
    if arena.winner:
        record = {'turns': arena._round,
                  'u1_name': arena.winner.get_name,
                  'u1_class': arena.winner._unit_type,
                  'u1_weapon_id': arena.winner._weapon.id,
                  'u1_armor_id': arena.winner._armor.id,
                  'u2_name': arena.loser.get_name,
                  'u2_class': arena.loser._unit_type,
                  'u2_weapon_id': arena.loser._weapon.id,
                  'u2_armor_id': arena.loser._armor.id,
                  }
        hall_of_fame_service.create_new(record)
    return redirect(location='/hall-of-fame/')


@main_blueprint.route('/hall-of-fame/', methods=['GET'])
def page_hall_of_fame():
    arena.get_clean()
    records = hall_of_fame_service.get_all()
    hall_of_fame = []
    for rec in records:
        rec = f'{rec.u1_class} {rec.u1_name} сразился с ' \
              f'{rec.u2_class} {rec.u2_name} и победил за ' \
              f'{rec.turns} ударов.'
        hall_of_fame.append(rec)

    # hall_of_fame = ['Первый результат боя', 'второй результат боя']
    return render_template('hall_of_fame.html', hall_of_fame=hall_of_fame)
