from app.app import create_app
from app.config import Config
from app.dao.models.armor import ArmorModel
from app.dao.models.weapon import WeaponModel
# from app.dao.models.classtype import ClassTypeModel as CT
from app.setup.db import db
from load_data import equipment

app = create_app(Config())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print('Таблицы созданы')

        weapons: list[WeaponModel] = []
        for weapon in equipment.weapons:
            weapons.append(WeaponModel(**weapon.dict()))
        armors: list[ArmorModel] = []
        for armor in equipment.armors:
            armors.append(ArmorModel(**armor.dict()))

        db.session.add_all(weapons)
        db.session.add_all(armors)
        # db.session.add_all([CT('Воин'), CT('Вор'), CT('Священник')])

        db.session.commit()
