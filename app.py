import math
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
receipts = {}

def count_alphanumeric(s):
    return sum(c.isalnum() for c in s)

def is_round_dollar(total):
    try:
        return float(total).is_integer()
    except Exception:
        return False

def is_multiple_of_025(total):
    try:
        return (float(total) * 100) % 25 == 0
    except Exception:
        return False

def points_for_items(items):
    return (len(items) // 2) * 5

def points_for_item_descriptions(items):
    points = 0
    for item in items:
        desc = item.get('shortDescription', '').strip()
        if len(desc) % 3 == 0:
            try:
                price = float(item.get('price', '0'))
                points += math.ceil(price * 0.2)
            except Exception:
                continue
    return points

def total_greater_than_10(total):
    try:
        return float(total) > 10.0
    except Exception:
        return False

def day_is_odd(date_str):
    try:
        day = int(date_str.split('-')[2])
        return day % 2 == 1
    except Exception:
        return False

def time_between_14_and_16(time_str):
    try:
        hour, minute = map(int, time_str.split(':'))
        return (hour == 14 and minute >= 0) or (hour == 15)
    except Exception:
        return False

def validate_receipt(receipt):
    # Check required fields
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    for field in required_fields:
        if field not in receipt:
            return False
    # Check items is a list with at least 1 item
    if not isinstance(receipt["items"], list) or len(receipt["items"]) < 1:
        return False
    # Check each item has required fields
    for item in receipt["items"]:
        if not isinstance(item, dict):
            return False
        if "shortDescription" not in item or "price" not in item:
            return False
    # Check total is string matching ^\d+\.\d{2}$
    import re
    if not isinstance(receipt["total"], str) or not re.match(r"^\d+\.\d{2}$", receipt["total"]):
        return False
    # Check purchaseDate and purchaseTime are strings
    if not isinstance(receipt["purchaseDate"], str) or not isinstance(receipt["purchaseTime"], str):
        return False
    return True

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    receipt = request.get_json()
    if not receipt or not validate_receipt(receipt):
        return jsonify({"error": "Invalid receipt. Please verify input."}), 400
    points = calculate_points(receipt)
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = points
    return jsonify({"id": receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts.get(receipt_id)
    if points is None:
        return jsonify({"error": "No receipt found for that ID."}), 404
    return jsonify({"points": points})

def calculate_points(receipt):
    points = 0
    points += count_alphanumeric(receipt.get('retailer', ''))
    if is_round_dollar(receipt.get('total', '0')):
        points += 50
    if is_multiple_of_025(receipt.get('total', '0')):
        points += 25
    items = receipt.get('items', [])
    points += points_for_items(items)
    points += points_for_item_descriptions(items)
    # LLM rule: 5 points if total > 10.00
    if total_greater_than_10(receipt.get('total', '0')):
        points += 5
    if day_is_odd(receipt.get('purchaseDate', '')):
        points += 6
    if time_between_14_and_16(receipt.get('purchaseTime', '')):
        points += 10
    return points

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
