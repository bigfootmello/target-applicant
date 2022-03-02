from . import db, ma
from marshmallow_sqlalchemy import fields


t_inventory = db.Table('Inventory',
                       db.Column('ProductID', db.Integer, db.ForeignKey('product.ProductID')),
                       db.Column('LocationID', db.Integer, db.ForeignKey('location.LocationID'))
                       )


# Product Table
class Product(db.Model):
    #__tablename__ = "Product"
    ProductID = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(30), unique=True, nullable=False)
    Description = db.Column(db.String(5000), nullable=False)
    SKU = db.Column(db.String(16), unique=True, nullable=False)
    OnlineOnly = db.Column(db.Boolean(), nullable=False)
    InStoreOnly = db.Column(db.Boolean(), nullable=False)
    inventory = db.relationship('Location', secondary=t_inventory, backref="products")

    def __repr__(self):
        return f"{self.Name} - {self.SKU} - {self.Description} - {self.OnlineOnly} - {self.InStoreOnly}"


# Location Table
class Location(db.Model):
    #__tablename__ = "Location"
    LocationID = db.Column(db.Integer, primary_key=True, nullable=False)
    Name = db.Column(db.String(30), nullable=False)
    Address = db.Column(db.Text(), nullable=False)
    City = db.Column(db.Text(), nullable=False)
    State = db.Column(db.String(2), nullable=False)
    Zip = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.Name} - {self.Address} - {self.City} - {self.State}, {self.Zip}"


class LocationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        include_fk = True


class ProductsSchema(ma.SQLAlchemyAutoSchema):
    inventory = ma.Nested(LocationsSchema)

    class Meta:
        model = Product


class RelationshipSchema(ma.SQLAlchemyAutoSchema):
    locationData = fields.Nested(LocationsSchema)
    productsData = fields.Nested(ProductsSchema)
