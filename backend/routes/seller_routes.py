from flask import Blueprint, request, jsonify
import boto3
import datetime

seller_bp = Blueprint('seller', __name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
category_table = dynamodb.Table('Category')
promo_table = dynamodb.Table('Promo')  # ✅ 确保 DynamoDB 中有这个表

# 获取商品分类
@seller_bp.route('/categories', methods=['GET'])
def get_categories():
    response = category_table.scan()
    categories = response.get('Items', [])
    return jsonify(categories), 200

# 发放优惠码
@seller_bp.route('/create-promo', methods=['POST'])
def create_promo():
    data = request.get_json()
    required = ['code', 'discount', 'created_by']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    item = {
        'code': data['code'],
        'discount': str(data['discount']),  # 可是字符串，也可以用 Decimal
        'created_by': data['created_by'],
        'created_at': datetime.datetime.utcnow().isoformat()
    }

    if 'expires_at' in data:
        item['expires_at'] = data['expires_at']

    promo_table.put_item(Item=item)
    return jsonify({'message': 'Promo created successfully'}), 200

@seller_bp.route('/seller/give-promo', methods=['POST'])
def give_promo():
    data = request.get_json()
    required = ['code', 'discount', 'seller_email']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    promo_table = dynamodb.Table('Promo')
    promo_table.put_item(Item={
        'code': data['code'],
        'discount': str(data['discount']),
        'seller_email': data['seller_email']
    })
    return jsonify({'message': 'Promo code created successfully'}), 200
