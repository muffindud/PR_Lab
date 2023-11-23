# init_db.py

# from app import app
from src.FlaskInstance import app

from models.databse import db
from models.electro_scooter import ElectroScooter


db_uris = [
    'postgresql://postgres:postgres@localhost:5432/scooters1',
    'postgresql://postgres:postgres@localhost:5432/scooters2',
    'postgresql://postgres:postgres@localhost:5432/scooters3'
]


def main():
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uris[2]
    db.init_app(app)

    with app.app_context():
        db.create_all()

        sample_scooter_1 = ElectroScooter('Scooter 1', 88.6)
        sample_scooter_2 = ElectroScooter('Scooter 2', 66.6)
        sample_scooter_3 = ElectroScooter('Scooter 3', 69.0)
        sample_scooter_4 = ElectroScooter('Scooter 4', 42.0)

        db.session.add(sample_scooter_1)
        db.session.add(sample_scooter_2)
        db.session.add(sample_scooter_3)
        db.session.add(sample_scooter_4)

        db.session.commit()


if __name__ == '__main__':
    main()
