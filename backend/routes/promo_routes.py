from flask import Blueprint, request, jsonify
import boto3

promo_bp = Blueprint('promo', __name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
promo_table = dynamodb.Table('Promo')

# GET /validate-promo?code=XXX
@promo_bp.route('/validate-promo', methods=['GET'])
def validate_promo():
    code = request.args.get('code')
    if not code:
        return jsonify({'valid': False, 'message': 'Missing promo code'}), 400

    try:
        response = promo_table.get_item(Key={'code': code})
        if 'Item' not in response:
            return jsonify({'valid': False, 'message': 'Invalid promo code'}), 404

        promo = response['Item']
        return jsonify({'valid': True, 'discount': promo.get('discount', '0')}), 200

    except Exception as e:
        return jsonify({'valid': False, 'message': str(e)}), 500
