from flask import Flask
from flask import current_app as app
from flask import jsonify
from flask_restful import Resource, abort, fields, marshal_with, reqparse

from .models import Location, Product, ProductsSchema, db


put_product_parser = reqparse.RequestParser()
put_product_parser.add_argument("Name", type=str, help="Name of the product is required", required=True)
put_product_parser.add_argument("Description", type=str, help="Description of product is required", required=True)
put_product_parser.add_argument("SKU", type=str, help="Product SKU", required=True)
put_product_parser.add_argument("OnlineOnly", type=bool, help="Product online only", required=True)
put_product_parser.add_argument("InStoreOnly", type=bool, help="Product in store only", required=True)

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument("Name", type=str, help="Name of the product")
update_product_parser.add_argument("Description", type=str, help="Description of product")
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


@app.route("/")
def Index():
    return jsonify({'My_Retail': 'API'})


@app.route('/api/product/<product_name>', methods=['GET'])
def get_product_by_name(product_name):
    result = Product.query.filter(Product.Name.contains(product_name)).all()
    product_schema = ProductsSchema(many=True)
    output = product_schema.dump(result)

    return {"Products": output}


@app.route("/api/product/locations/<location_id>", methods=['GET'])
def get_product_by_location(location_id):
    results = db.session.query(Location.LocationID, Location.Name, Product.Name).select_from(Product)\
        .join(Product.inventory)\
        .filter(Location.LocationID == location_id).all()
    product_schema = ProductsSchema(many=True)
    output = product_schema.dump(results)

    return {"Products": output}


@app.route('/api/product/<product_id>', methods=['PATCH'])
def update_product(product_id):
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
    return str(result)


@app.route('/api/product/<product_id>', methods=['PUT'])
def add_product(product_id):
    args = put_product_parser.parse_args()
    result = Product(ProductID=product_id, Name=args['Name'], Description=args['Description'], SKU=args['SKU'],
                     OnlineOnly=args['OnlineOnly'], InStoreOnly=args['InStoreOnly'])
    db.session.add(result)
    db.session.commit()
    return str(result), 201


@app.route('/api/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = Product.query.filter_by(ProductID=product_id).first()
    if not result:
        abort(404, message="Product not found, unable to delete.")
    db.session.delete(result)
    db.session.commit()
    return '', 204
