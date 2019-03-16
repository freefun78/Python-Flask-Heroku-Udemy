from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                       type=float,
                       required=True,
                       help="This field is required, cannot be left blank !")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store ID field is required, cannot be left blank !")



    def post(self, name):
        if ItemModel.get_item_by_name(name):
            # HTTP Code 400 : Bad request.
            return {"message": "item '{}' already exists.".format(name)}, 404

        data = Item.parser.parse_args()
        new_item = ItemModel(name, data["price"], data["store_id"])
        try :
            new_item.save_to_db()
        except:
            # HTTP Code 500: Internal server error
            return {"message": "Error inserting item !"}, 500

        # HTTP Code 201: Item Creation OK
        return new_item.json(), 201

    @jwt_required()
    def get(self, name):
        item_to_get = ItemModel.get_item_by_name(name)

        if not item_to_get:
            # HTP Code 404 : Not Found
            return {"message": "Item not found."}, 404

        # HTTP Code 200, OK
        return {"items": item_to_get.json()}, 200

    def put(self, name):
        data = Item.parser.parse_args()

        item_to_put = ItemModel.get_item_by_name(name)
        if item_to_put :
            try:
                item_to_put.price = data['price']
                item_to_put.store_id = data['store_id']
                item_to_put.save_to_db()
            except:
                # HTTP Code 500: Internal server error
                return {"message": "Error updating item !"},500
        else :
            try:
                item_to_put = ItemModel(name, data["price"], data['store_id'])
                item_to_put.save_to_db()
            except:
                # HTTP Code 500: Internal server error
                return {"message": "Error inserting item !"}, 500

        return item_to_put.json();

    def delete(self,name):

        item_to_delete =  ItemModel.get_item_by_name(name)

        if item_to_delete is None :
            # HTTP Code 400 : Bad Request
            return {"message": "Item to delete is not found"}, 400

        try :
            item_to_delete.delete_from_db()
        except :
            # HTTP Code 500: Internal server error
            return {"message": "Error deleting item"}, 500

        # HTTP Code 200 : OK
        return {"message": "Item is deleted successfully"}, 200


class ItemList(Resource) :

    def get(self):
        # Using Lambda
        #return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}, 200

        # Using list comprehension.
        return {"items": [ item.json() for item in ItemModel.query.all()]}, 200