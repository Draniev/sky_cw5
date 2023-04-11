from app.app import create_app
from app.config import Config
from app.setup.db import db

app = create_app(Config())

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        print('Таблицы удалены')
