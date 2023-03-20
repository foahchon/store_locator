from flask import Blueprint, jsonify, request, abort
from ..models import Vendor, Member, db

bp = Blueprint('vendors', __name__, url_prefix='/vendors')

@bp.route('/', methods=['GET'])
def index():
    vendors = Vendor.query.all()
    result = []

    for v in vendors:
        result.append(v.serialize())

    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
     v = Vendor.query.get_or_404(id)

     return jsonify(v.serialize())

@bp.route('<int:vendor_id>/stores')
def get_stores_for_vendor(vendor_id: int):
    v = Vendor.query.get_or_404(vendor_id)
    result = []

    for s in v.stores:
        result.append(s.serialize())

    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json or \
        'street_address' not in request.json or \
        'city' not in request.json or \
        'state' not in request.json or \
        'zip_code' not in request.json or \
        'member_id' not in request.json <= 0:
        return abort(400)
    
    if len(request.json['name']) <= 0 or \
        len(request.json['street_address']) <= 0 or \
        len(request.json['city']) <= 0 or \
        len(request.json['state']) != 2 or \
        len(request.json['zip_code']) != 5 or \
        request.json['member_id'] <= 0:
        return abort(400)
    
    v = Vendor(
          name=request.json['name'],
          street_address=request.json['street_address'],
          city=request.json['city'],
          state=request.json['state'],
          zip_code=request.json['zip_code'],
          member_id=request.json['member_id']
    )

    db.session.add(v)
    db.session.commit()

    return jsonify(v.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    v = Vendor.query.get_or_404(id)

    try:
        db.session.delete(v)
        db.session.commit()

        return jsonify(True)

    except:
            return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    v = Vendor.query.get_or_404(id)

    if 'name' in request.json:
        if len(request.json['name']) <= 0:
            return abort(400)
        
        v.name = request.json['name']

    if 'street_address' in request.json:
        if len(request.json['street_address']) <= 0:
            return abort(400)

        v.street_address = request.json['street_address']

    if 'city' in request.json:
        if len(request.json['city']) <= 0:
            return abort(400)

        v.city = request.json['city']

    if 'state' in request.json:
        if len(request.json['state']) != 2:
            return abort(400)

        v.state = request.json['state']

    if 'zip_code' in request.json:
        if len(request.json['zip_code']) != 5:
            return abort(400)

        v.zip_code = request.json['zip_code']

    if 'member_id' in request.json:
        v.member_id = request.json['member_id']

    try:
        db.session.commit()

        return jsonify(v.serialize())
    
    except:
        return jsonify(False)
    
@bp.route('/<int:id>/products', methods=['GET'])
def get_products_for_vendor(id: int):
    v = Vendor.query.get_or_404(id)
    result = []

    for p in v.products:
        result.append(p.serialize())

    return jsonify(result)