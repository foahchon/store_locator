from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"

db = SQLAlchemy()

stores_products_table = db.Table('stores_products',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

vendors_stores_table = db.Table('vendors_stores',
    db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
    db.Column('vendor_id', db.Integer, db.ForeignKey('vendors.id'), primary_key=True)
)

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), unique=False, nullable=False)
    vendors = db.relationship('Vendor', backref='member', cascade='all,delete')
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow(), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    street_address = db.Column(db.String(), unique=False, nullable=False)
    city = db.Column(db.String(), unique=False, nullable=False)
    state = db.Column(db.String(2), unique=False, nullable=False)
    zip_code = db.Column(db.String(5), unique=False, nullable=False)
    products = db.relationship('Product', backref='vendor', cascade='all,delete')
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    stores = db.relationship('Store', secondary=vendors_stores_table, back_populates='vendors')
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow(), nullable=False)

    def __init__(self, name, street_address, city, state, zip_code, member_id):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.member_id = member_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'street_address': self.street_address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'member_id': self.member_id
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    price = db.Column(db.Numeric(), unique=False, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    stores = db.relationship('Store', secondary=stores_products_table, back_populates='products')
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow(), nullable=False)

    def __init__(self, name, description, price, vendor_id):
        self.name = name
        self.description = description
        self.price = price
        self.vendor_id = vendor_id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'vendor_id': self.vendor_id
        }

class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    street_address = db.Column(db.String(), unique=False, nullable=False)
    city = db.Column(db.String(), unique=False, nullable=False)
    state = db.Column(db.String(2), unique=False, nullable=False)
    zip_code = db.Column(db.String(5), unique=False, nullable=False)
    latitude = db.Column(db.Numeric(), unique=False, nullable=False)
    longitude = db.Column(db.Numeric(), unique=False, nullable=False)
    products = db.relationship('Product', secondary=stores_products_table, back_populates='stores')
    vendors = db.relationship('Vendor', secondary=vendors_stores_table, back_populates='stores')
    created_at = db.Column(db.DateTime(timezone=True), default=utcnow(), nullable=False)

    def __init__(self, name, street_address, city, state, zip_code, latitude, longitude):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.latitude = latitude
        self.longitude = longitude

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'street_address': self.street_address,
            'city': self.city,
            'zip_code': self.zip_code,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude)
        }