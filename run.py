import logging

from app.app import create_app
from app.config import Config

app = create_app(Config())

logger = logging.getLogger('arena')
console_handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel('DEBUG')

if __name__ == "__main__":
    app.run()
