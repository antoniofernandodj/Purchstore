from purchstore.scrapper import Scrapper
from purchstore.database import db


if __name__ == "__main__":
    db.criar_banco_de_dados()
    app = Scrapper(image_dir='images')
    app.run()
