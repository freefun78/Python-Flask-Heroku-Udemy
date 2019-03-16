from db import db

class ItemModel(db.Model) :

    __tablename__ = 'items'
    id = db.Column( db.Integer, primary_key=True)
    name = db.Column( db.String(80))
    price = db.Column( db.Float( precision=2))
    store_id = db.Column( db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id) :
        self.name = name
        self.price = price
        self.store_id = store_id


    def json(self):
        # If returning self.store.json() <- this will create never ending loop as the store_model also call item_model too.
        return {"name": self.name, "price": self.price, "store_id": self.store_id, "store_name": self.store.name}

    @classmethod
    def get_item_by_name(cls, name):
        # SQLLite query way
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # qresult = cursor.fetchone()
        # connection.close()
        # if qresult:
        #     return cls(qresult[0], qresult[1], qresult[2])
        # else:
        #     return None
        return ItemModel.query.filter_by(name=name).first() # SELECT * from users where name = name LIMIT 1;


    def save_to_db(self):
        # SQLITE3 ways
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES(NULL, ?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close

        # For both insert & update
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # SQLITE3 version
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "DELETE FROM items " \
        #         "WHERE name = ?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        db.session.delete(self)
        db.session.commit()
