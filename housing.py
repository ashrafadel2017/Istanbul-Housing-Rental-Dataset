import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql = """
        CREATE TABLE IF NOT EXISTS housing(
            id Integer Primary Key,
            neighbourhood text,
            latitude text,
            longitude text,
            room_type text,
            price text,
            minimum_nights text,
            number_of_reviews text,
            last_review text,
            reviews_per_month text,
            calculated_host_listings_count text,
            availability_365 text,
            number_of_reviews_ltm text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, neighbourhood, latitude, longitude, room_type, price,
               minimum_nights, number_of_reviews, last_review,
               reviews_per_month, calculated_host_listings_count,
               availability_365, number_of_reviews_ltm):
        self.cur.execute(
            """INSERT INTO housing VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (neighbourhood, latitude, longitude, room_type, price,
             minimum_nights, number_of_reviews, last_review,
             reviews_per_month, calculated_host_listings_count,
             availability_365, number_of_reviews_ltm)
        )
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM housing")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM housing WHERE id=?", (id,))
        self.con.commit()

    def update(self, id, neighbourhood, latitude, longitude, room_type, price,
               minimum_nights, number_of_reviews, last_review,
               reviews_per_month, calculated_host_listings_count,
               availability_365, number_of_reviews_ltm):
        self.cur.execute(
            """UPDATE housing SET 
               neighbourhood=?, latitude=?, longitude=?, room_type=?, price=?, 
               minimum_nights=?, number_of_reviews=?, last_review=?, 
               reviews_per_month=?, calculated_host_listings_count=?, 
               availability_365=?, number_of_reviews_ltm=? 
               WHERE id=?""",
            (neighbourhood, latitude, longitude, room_type, price,
             minimum_nights, number_of_reviews, last_review,
             reviews_per_month, calculated_host_listings_count,
             availability_365, number_of_reviews_ltm, id)
        )
        self.con.commit()
