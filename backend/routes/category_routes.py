from flask import Blueprint, request, jsonify
import boto3

category_bp = Blueprint('category', __name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
category_table = dynamodb.Table('Category')

@category_bp.route('/add-category', methods=['POST'])
def add_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Missing category name'}), 400

    category_table.put_item(Item={'name': name})
    return jsonify({'message': 'Category added'}), 200

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    response = category_table.scan()
    return jsonify(response.get('Items', [])), 200
