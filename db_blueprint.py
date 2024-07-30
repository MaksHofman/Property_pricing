import sqlite3
from datetime import datetime, timedelta
import time

def get_date_now() -> datetime:
    return datetime.now()
def creating_db():
    def connect_to_db():
        conn = sqlite3.connect('home_scrapper.db')
        c = conn.cursor()
        return c, conn

    def creating_db_homes(c, conn):

        # creating main table(currently place holder)
        c.execute('''
            CREATE TABLE IF NOT EXISTS homes (
                id_otodom INTEGER PRIMARY KEY NOT NULL,
                city TEXT NOT NULL,
                district TEXT NOT NULL,
                street TEXT NOT NULL,
                price INTEGER NOT NULL,
                rooms INTEGER NOT NULL,
                square_area FLOAT NOT NULL,
                price_for_square_meter INTEGER NOT NULL,
                floor INTEGER NOT NULL,
                rent INTEGER,
                ownership TEXT NOT NULL,
                finish_condition TEXT NOT NULL,
                balcony_garden_terrace TEXT NOT NULL,
                parking_space TEXT NOT NULL,
                heating TEXT NOT NULL,
                amount_of_pictures INTEGER NOT NULL,
                published_date DATE NOT NULL,
                description TEXT NOT NULL,
                lift TEXT,
                market_type TEXT,
                advertiser_type TEXT,
                available_from DATE,
                year_of_construction INTEGER,
                phone_number TEXT,
                building_type TEXT,
                windows TEXT,
                media TEXT,
                security_type TEXT,
                equipment TEXT,
                extra_info TEXT,
                building_material TEXT,
                owners_name TEXT
            )
        ''')
        conn.commit()


    if __name__ == '__main__':
        c,conn = connect_to_db()
        creating_db_homes(c, conn)
        conn.close()

if __name__ == '__main__':
    creating_db()