from flask import Blueprint, jsonify, request
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import boto3
import uuid
from boto3.dynamodb.conditions import Attr

product_bp = Blueprint('product', __name__)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
product_table = dynamodb.Table('Products')

# 获取某一分类的最多6个商品
@product_bp.route('/products-by-category/<category>', methods=['GET'])
def get_products_by_category(category):
    response = product_table.scan(
        FilterExpression=Attr('category').eq(category)
    )
    items = response.get('Items', [])
    return jsonify(items[:6]), 200

# 添加商品（用于卖家上传商品）
@product_bp.route('/add-product', methods=['POST'])
def add_product():
    data = request.get_json()
    required = ['name', 'price', 'category', 'image_url', 'stock', 'seller_id']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    product = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'price': Decimal(str(data['price'])),  # Decimal requires string or float
        'category': data['category'],
        'image_url': data['image_url'],
        'stock': int(data['stock']),
        'seller_id': data['seller_id'],
        'description': data.get('description', '')
    }

    product_table.put_item(Item=product)
    return jsonify({'message': 'Product added'}), 200

@product_bp.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    response = product_table.get_item(Key={'id': product_id})
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(item), 200
