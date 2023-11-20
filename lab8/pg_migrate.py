# ./
# pg_migrate.py
from sqlalchemy import create_engine, select
from app import app

from models.databse import db
from models.electro_scooter import ElectroScooter


sqlite_engine = create_engine('sqlite:///instance/database.db')
pg_engine = create_engine('postgresql://postgres:postgres@localhost:5432/scooters')


def main():
    with sqlite_engine.connect() as sqlite_conn:
        with pg_engine.connect() as pg_conn:
            with app.app_context():
                db.init_app(app)
                for table in ElectroScooter.metadata.sorted_tables:
                    data = [row for row in sqlite_conn.execute(select(table.c))]
                    print(table)
                    print(data)
                    for row in data:
                        db.session.add(ElectroScooter(row[1], row[2]))
                db.session.commit()


if __name__ == "__main__":
    main()
