from purchstore.scrapper import Scrapper
from purchstore.database import db
import json

with open('codes.json') as f:
    CODES = json.load(f)


if __name__ == "__main__":
    db.criar_banco_de_dados()
    app = Scrapper()
    app.parse_images(image_dir='images')
    app.parse_codes(codes=CODES)
