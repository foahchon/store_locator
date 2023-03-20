from flask import Blueprint, jsonify, request, abort
from ..models import Member, db
import re
import hashlib
import secrets


def scramble(password: str) -> str:
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)

    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


def validate_email(email: str) -> bool:
    return re.search(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email)

bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('', methods=['GET'])
def index():
    members = Member.query.all()
    result = []

    for m in members:
        result.append(m.serialize())

    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    m = Member.query.get_or_404(id)

    return jsonify(m.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'email' in request.json and 'name' in request.json and 'password' in request.json:
        if not validate_email(request.json['email']) or len(request.json['password']) < 6 or len(request.json['name']) <= 0:
            return abort(400)
        
        m = Member(
            email=request.json['email'],
            name=request.json['name'],
            password=scramble(request.json['password'])
        )

        db.session.add(m)
        db.session.commit()

        return jsonify(m.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    m = Member.query.get_or_404(id)

    try:
        db.session.delete(m)
        db.session.commit()

        return jsonify(True)

    except:
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    m = Member.query.get_or_404(id)

    if 'email' not in request.json and 'password' not in request.json:
        return abort(400)
    
    if not validate_email(request.json['email']):
        return abort(400)
    
    m.email = request.json['email']

    if len(request.json['password']) < 6:
        return abort(400)
        
    m.password = scramble(request.json['password'])

    if len(request.json['name']) <= 0:
        return abort(400)
        
    m.name = request.json['name']

    try:
        db.session.commit()

        return jsonify(m.serialize())
    
    except:
        return jsonify(False)
    
@bp.route('/<int:member_id>/vendors')
def get_vendors_for_member(member_id: int):
    m = Member.query.get_or_404(member_id)
    result = []

    for v in m.vendors:
        result.append(v.serialize())

    return jsonify(result)