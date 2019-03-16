from flask_restful import Resource, reqparse
from models.store_model import StoreModel

class Store(Resource) :
    parser = reqparse.RequestParser()
    parser.add_argument( 'name',
                         type=str,
                         required=True,
                         help="Store name is required, cannot be left blank !")

    def get(self, name):
        store_to_find = StoreModel.get_store_by_name(name)
        if store_to_find is None :
            return {"message": "Store with name '{}' does not exist".format(name)}, 404
        return store_to_find.json()

    def post(self, name):
        store_to_find = StoreModel.get_store_by_name(name)
        if store_to_find :
            return {"message": "Store with name '{}' already exists".format(name)}, 400

        store_to_find = StoreModel(name)
        try :
            store_to_find.save_to_db()
        except :
            return {"message": "Error saving store to db."}, 500

        return store_to_find.json(), 201

    def delete(self, name):
        store_to_find = StoreModel.get_store_by_name(name)
        if store_to_find is None :
            return {"message": "Store with name '{}' does not exist".format(name)}, 404

        try :
            store_to_find.delete_from_db()
        except :
            return {"message" : "Error deleting store"}, 500

        return {"message": "Store '{}' is deleted successfully".format(name)}

class StoreList(Resource) :

    def get(self):
        return { "stores" : [store.json() for store in StoreModel.query.all()]}