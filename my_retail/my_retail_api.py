from flask import Flask, jsonify
from flask import current_app as app
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from . import api
from .models import db, Product, Location

@app.route("/")
def Index():
    return jsonify({'Hello': 'World!'})

# from flask import Flask, request
# from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# # app.config.from_object('config.DevConfig')
# # app.config.from_object('config.ProdConfig')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///My_RETAIL.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

# api = Api(app)
# db = SQLAlchemy(app)


# t_inventory = db.Table('Inventory',
#                        db.Column('ProductID', db.Integer, db.ForeignKey('product.ProductID')),
#                        db.Column('LocationID', db.Integer, db.ForeignKey('location.LocationID'))
#                        )


# # Product Table
# class Product(db.Model):
#     ProductID = db.Column(db.Integer, primary_key=True, nullable=False)
#     Name = db.Column(db.String(30), unique=True, nullable=False)
#     Description = db.Column(db.String(5000), nullable=False)
#     SKU = db.Column(db.String(16), unique=True, nullable=False)
#     OnlineOnly = db.Column(db.Boolean(), nullable=False)
#     InStoreOnly = db.Column(db.Boolean(), nullable=False)
#     inventory = db.relationship('Location', secondary=t_inventory, backref="products")

#     def __repr__(self):
#         return f"{self.Name} - {self.SKU} - {self.Description} - {self.OnlineOnly} - {self.InStoreOnly}"


# # Location Table
# class Location(db.Model):
#     LocationID = db.Column(db.Integer, primary_key=True, nullable=False)
#     Name = db.Column(db.String(30), nullable=False)
#     Address = db.Column(db.Text(), nullable=False)
#     City = db.Column(db.Text(), nullable=False)
#     State = db.Column(db.String(2), nullable=False)
#     Zip = db.Column(db.String(10), nullable=False)

#     def __repr__(self):
#         return f"{self.Name} - {self.Address} - {self.City} - {self.State}, {self.Zip}"


# class LocationsSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Location
#         include_fk = True
#
#
# class ProductsSchema(ma.SQLAlchemyAutoSchema):
#     inventory = ma.Nested(LocationsSchema)
#
#     class Meta:
#         model = Product
#
#
# class RelationshipSchema(ma.SQLAlchemyAutoSchema):
#     locationData = fields.Nested(LocationsSchema)
#     productsData = fields.Nested(ProductsSchema)


put_product_parser = reqparse.RequestParser()
put_product_parser.add_argument("Name", type=str, help="Name of the product is required", required=True)
put_product_parser.add_argument("Description", type=str, help="Description of product is required")
put_product_parser.add_argument("SKU", type=str, help="Product SKU")
put_product_parser.add_argument("OnlineOnly", type=bool, help="Product online only")
put_product_parser.add_argument("InStoreOnly", type=bool, help="Product in store only")

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument("Name", type=str, help="Name of the product is required")
update_product_parser.add_argument("Description", type=str, help="Description of product is required")
update_product_parser.add_argument("SKU", type=str, help="Product SKU")
update_product_parser.add_argument("OnlineOnly", type=bool, help="Product online only")
update_product_parser.add_argument("InStoreOnly", type=bool, help="Product in store only")

# Define object serialization
resource_fields = {
    'ProductID': fields.Integer,
    'Name': fields.String,
    'Description': fields.String,
    'SKU': fields.String,
    'OnlineOnly': fields.Boolean,
    'InStoreOnly': fields.Boolean
}


class Retail(Resource):
    @marshal_with(resource_fields)
    def get(self, product_name):
        result = Product.query.filter(Product.Name.contains(product_name)).all()
        if not result:
            abort(404, message="Product not found")
        return result

    @marshal_with(resource_fields)
    def put(self, product_id):
        args = put_product_parser.parse_args()
        result = Product(ProductID=product_id, Name=args['Name'], Description=args['Description'], SKU=args['SKU'],
                         OnlineOnly=args['OnlineOnly'], InStoreOnly=args['InStoreOnly'])
        db.session.add(result)
        db.session.commit()
        return result, 201

    @marshal_with(resource_fields)
    def patch(self, product_id):
        args = update_product_parser.parse_args()
        result = Product.query.filter_by(ProductID=product_id).first()
        if not result:
            abort(404, message="Product not found, unable to update")

        if args['Name']:
            result.Name = args['Name']
        if args['Description']:
            result.Description = args['Description']
        if args['SKU']:
            result.SKU = args['SKU']
        if args['OnlineOnly']:
            result.OnlineOnly = args['OnlineOnly']
        if args['InStoreOnly']:
            result.InStoreOnly = args['InStoreOnly']

        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def delete(self, product_id):
        result = Product.query.filter_by(ProductID=product_id).first()
        if not result:
            abort(404, message="Product not found, unable to delete")
        db.session.delete(result)
        db.session.commit()
        return '', 204


class ReturnProductLocation(Resource):
    @marshal_with(resource_fields)
    def get(self, location_id):
        result = db.session.query(Location.LocationID, Location.Name, Product.Name).select_from(Product)\
            .join(Product.inventory)\
            .filter(Location.LocationID == location_id)\
            .all()
        if not result:
            abort(404, message="Product not found")

        return result

class Tester(Resource):
    def get(self):
        return jsonify({'Hello': 'World!'})


api.add_resource(Retail, "/api/product/<int:product_id>", "/api/product/<string:product_name>")
api.add_resource(ReturnProductLocation, "/api/product_location/<int:location_id>")
api.add_resource(Tester, "/api/")
