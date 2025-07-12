from flask import Blueprint, request, jsonify
from .models import db, User, Skill, SwapRequest
from .utils import hash_password, verify_password

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Email or name already exists'}), 400
    user = User()
    user.email = data['email']
    user.password = hash_password(data['password'])
    user.name = data['name']
    user.location = data.get('location')
    user.profile_photo = data.get('profile_photo')
    user.availability = data.get('availability')
    user.public = data.get('public', True)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and verify_password(data.get('password'), user.password):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/skills', methods=['POST'])
def add_skill():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Skill name required'}), 400
    if Skill.query.filter_by(name=name).first():
        return jsonify({'error': 'Skill already exists'}), 400
    skill = Skill()
    skill.name = name
    db.session.add(skill)
    db.session.commit()
    return jsonify({'message': 'Skill added', 'skill_id': skill.id})

@bp.route('/swap', methods=['POST'])
def create_swap():
    data = request.get_json()
    requestor_id = data.get('requestor_id')
    receiver_id = data.get('receiver_id')
    if not requestor_id or not receiver_id:
        return jsonify({'error': 'Missing user IDs'}), 400
    swap = SwapRequest()
    swap.requestor_id = requestor_id
    swap.receiver_id = receiver_id
    db.session.add(swap)
    db.session.commit()
    return jsonify({'message': 'Swap request created', 'swap_id': swap.id}) 