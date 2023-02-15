from flask import Blueprint, jsonify
from flask_login import login_required
from models import Seed

shop = Blueprint('shop', __name__)

@shop.get('/shop')
def get_shop_items():
    """Returns JSON with all seeds available for purchase"""
    shop_list = Seed.query.all()
    shop_serialized = [item.serialize() for item in shop_list]
    return jsonify(shop=shop_serialized)

