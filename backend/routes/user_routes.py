from flask import Blueprint, request, jsonify
import boto3
import uuid
from decimal import Decimal

user_bp = Blueprint('user', __name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

cart_table = dynamodb.Table('Cart')
order_table = dynamodb.Table('Orders')
product_table = dynamodb.Table('Products')
promo_table = dynamodb.Table('Promo')

# 获取购物车内容
@user_bp.route('/cart/<email>', methods=['GET'])
def get_cart(email):
    response = cart_table.get_item(Key={'email': email})
    return jsonify({"success": True, "cart": response.get('Item', {}).get('items', [])})

# 添加商品到购物车
@user_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    email = data.get('email')
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    # 获取商品信息
    prod = product_table.get_item(Key={'id': product_id}).get('Item')
    if not prod:
        return jsonify({"success": False, "message": "Product not found"}), 404

    item = {
        "product_id": product_id,
        "name": prod['name'],
        "price": float(prod['price']),
        "quantity": quantity,
        "image_url": prod.get('image_url', '')
    }

    # 获取原购物车
    cart = cart_table.get_item(Key={'email': email}).get('Item', {})
    items = cart.get('items', [])

    # 如果已存在则叠加数量
    found = False
    for i in items:
        if i['product_id'] == product_id:
            i['quantity'] += quantity
            found = True
            break
    if not found:
        items.append(item)

    cart_table.put_item(Item={'email': email, 'items': items})
    return jsonify({"success": True})

# 移除商品
@user_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    email = data.get('email')
    product_id = data.get('product_id')

    cart = cart_table.get_item(Key={'email': email}).get('Item', {})
    items = cart.get('items', [])
    items = [i for i in items if i['product_id'] != product_id]

    cart_table.put_item(Item={'email': email, 'items': items})
    return jsonify({"success": True})

# 结账
@user_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    email = data.get('email')

    cart = cart_table.get_item(Key={'email': email}).get('Item', {})
    items = cart.get('items', [])

    if not items:
        return jsonify({"success": False, "message": "Cart is empty"}), 400

    total = sum(i['price'] * i['quantity'] for i in items)
    order = {
        "order_id": str(uuid.uuid4()),
        "email": email,
        "products": items,
        "total": float(round(total, 2)),
        "date": str(uuid.uuid1())
    }

    order_table.put_item(Item=order)
    cart_table.delete_item(Key={'email': email})
    return jsonify({"success": True, "order_id": order['order_id']})

# 获取历史订单
@user_bp.route('/orders/<email>', methods=['GET'])
def get_orders(email):
    response = order_table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr('email').eq(email)
    )
    return jsonify({"success": True, "orders": response.get('Items', [])})
