from flask import Blueprint, jsonify, request, abort
from ..models import Product, db

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/', methods=['GET'])
def index():
    products = Product.query.all()
    result = []

    for p in products:
        result.append(p.serialize())

    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Product.query.get_or_404(id)

    return jsonify(p.serialize())


@bp.route('/<int:product_id>/stores', methods=['GET'])
def get_stores_for_product(product_id: int):
    p = Product.query.get_or_404(product_id)
    result = []

    for s in p.stores:
        result.append(s.serialize())

    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json or \
        'description' not in request.json or \
        'price' not in request.json or \
        'vendor_id' not in request.json:
        return abort(400)
    
    if len(request.json['name']) <= 0 or \
        len(request.json['description']) <= 0 or \
        request.json['price'] <= 0 or \
        request.json['vendor_id'] <= 0:
        return abort(400)
    
    p = Product(
        name=request.json['name'],
        description=request.json['description'],
        price=request.json['price'],
        vendor_id=request.json['vendor_id']
    )

    try:
        db.session.add(p)
        db.session.commit()

        return jsonify(p.serialize())
    
    except:
        return jsonify(False)
    

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Product.query.get_or_404(id)

    try:
        db.session.delete(p)
        db.session.commit()

        return jsonify(True)

    except:
        return jsonify(False)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    p = Product.query.get_or_404(id)

    if 'name' in request.json:
        if len(request.json['name']) <= 0:
            return abort(400)

        p.name = request.json['name']

    if 'description' in request.json:
        if len(request.json['description']) <= 0:
            return abort(400)

        p.description = request.json['description']

    if 'price' in request.json:
        if request.json['price'] <= 0:
            return abort(400)

        p.price = request.json['price']
        
    try:
        db.session.commit()

        return jsonify(p.serialize())
    
    except:
        return jsonify(False)