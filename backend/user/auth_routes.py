from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
import boto3
import uuid

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# DynamoDB 表连接（你也可以从 models/db.py 里 import）
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
users_table = dynamodb.Table('Users')

# 注册接口
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 检查用户是否已存在
    response = users_table.get_item(Key={'email': email})
    if 'Item' in response:
        return jsonify({"error": "User already exists"}), 400

    # 密码加密
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

    # 存储用户信息
    users_table.put_item(Item={
        'email': email,
        'password': hashed_pw,
        'user_id': str(uuid.uuid4())
    })

    return jsonify({"message": "Signup successful"}), 200

# 登录接口
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 查询用户
    response = users_table.get_item(Key={'email': email})
    user = response.get('Item')

    if not user:
        return jsonify({"error": "User not found"}), 404

    # 验证密码
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"message": "Login successful"}), 200
