from flask import Blueprint, jsonify, request, abort
from ..models import Product, Store, Vendor, db

bp = Blueprint('stores', __name__, url_prefix='/stores')


@bp.route('/', methods=['GET'])
def index():
    stores = Store.query.all()
    result = []

    for s in stores:
        result.append(s.serialize())

    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    s = Store.query.get_or_404(id)

    return jsonify(s.serialize())

@bp.route('/<int:store_id>/products', methods=['GET'])
def get_products_for_store(store_id: int):
    s = Store.query.get_or_404(store_id)
    result = []

    for p in s.products:
        result.append(p.serialize())

    return jsonify(result)

@bp.route('/<int:store_id>/vendors', methods=['GET'])
def get_vendors_for_store(store_id: int):
    s = Store.query.get_or_404(store_id)
    result = []

    for v in s.vendors:
        result.append(v.serialize())

    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json or \
        'street_address' not in request.json or \
        'city' not in request.json or \
        'state' not in request.json or \
        'zip_code' not in request.json or \
        'latitude' not in request.json or \
        'longitude' not in request.json:
        return abort(400)

    if len(request.json['name']) <= 0 or \
        len(request.json['street_address']) <= 0 or \
        len(request.json['city']) <= 0 or \
        len(request.json['state']) != 2 or \
        len(request.json['zip_code']) != 5 or \
        not isinstance(request.json['latitude'], float) or \
        not isinstance(request.json['longitude'], float):
        return abort(400)

    s = Store(
        name=request.json['name'],
        street_address=request.json['street_address'],
        city=request.json['city'],
        state=request.json['state'],
        zip_code=request.json['zip_code'],
        latitude=request.json['latitude'],
        longitude=request.json['longitude']
    )

    try:
        db.session.add(s)
        db.session.commit()

        return jsonify(s.serialize())
    
    except:
        return jsonify(False)

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Store.query.get_or_404(id)

    try:
        db.session.delete(s)
        db.session.commit()

        return jsonify(True)
    
    except:
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    s = Store.query.get_or_404(id)

    if 'name' in request.json:
        if len(request.json['name']) <= 0:
            return abort(400)

        s.name = request.json['name']

    if 'street_address' in request.json:
        if len(request.json['street_address']) <= 0:
            return abort(400)

        s.street_address = request.json['street_address']

    if 'city' in request.json:
        if len(request.json['city']) <= 0:
            return abort(400)

        s.city = request.json['city']

    if 'state' in request.json:
        if len(request.json['state']) != 2:
            return abort(400)

        s.state = request.json['state']

    if 'zip_code' in request.json:
        if len(request.json['zip_code']) != 5:
            return abort(400)

        s.zip_code = request.json['zip_code']

    if 'latitude' in request.json:
        if not isinstance(request.json['latitude'], float):
            return abort(400)
        
        s.latitude = request.json['latitude']

    if 'longitude' in request.json:
        if not isinstance(request.json['longitude'], float):
            return abort(400)

        s.longitude = request.json['longitude']

    try:
        db.session.commit()

        return jsonify(s.serialize())

    except:
        return jsonify(False)

@bp.route('/<int:store_id>/product/<int:product_id>', methods=['POST', 'DELETE'])
def add_or_remove_product_to_or_from_store(store_id, product_id):
    s = Store.query.get_or_404(store_id)
    p = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        # only allow vendor's products to be added to store if
        # vendor is added to store first
        if p.vendor in s.vendors:
            s.products.append(p)
        else:
            return abort(400)
    elif request.method == 'DELETE':
        s.products.remove(p)
    else:
        return abort(400)

    try:
        db.session.commit()

        return jsonify(True)
    
    except:
        return jsonify(False)


@bp.route('/<int:store_id>/vendor/<int:product_id>', methods=['POST', 'DELETE'])
def add_or_remove_vendor_to_or_from_store(store_id, product_id):
    s = Store.query.get_or_404(store_id)
    v = Vendor.query.get_or_404(product_id)

    if request.method == 'POST':
        s.vendors.append(v)
    elif request.method == 'DELETE':
        # remove vendor's products from the store
        for p in v.products:
            if p in s.products:
                s.products.remove(p)
        s.vendors.remove(v)
    else:
        return abort(400)

    try:
        db.session.commit()

        return jsonify(True)

    except:
        return jsonify(False)
