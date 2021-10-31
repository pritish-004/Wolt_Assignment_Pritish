import json

import dateutil.parser

from flask import abort, Flask, jsonify, request

from backend.delivery_fee.delivery_fee_calculator import delivery_fee_calculator

app = Flask(__name__)


def validate_cart_data(cart_data):
    """ Validate if cart data has all the required fields and values """
    if 'cart_value' not in cart_data:
        abort(404, description="Missing argument cart value")

    if not isinstance(cart_data['cart_value'], int) or cart_data['cart_value'] <= 0:
        abort(400, description=f"Cart value = {cart_data['cart_value']} is not positive integer")

    if 'delivery_distance' not in cart_data:
        abort(404, description="Missing argument delivery distance")

    if not isinstance(cart_data['delivery_distance'], int) or cart_data['delivery_distance'] <= 0:
        abort(400, description=f"delivery distance = {cart_data['delivery_distance']} is not positive integer")

    if 'amount_of_items' not in cart_data:
        abort(404, description="Missing argument amount_of_items")

    if not isinstance(cart_data['amount_of_items'], int) or cart_data['amount_of_items'] <= 0:
        abort(400, description=f"amount of items = {cart_data['amount_of_items']} is not positive integer")

    if 'time' not in cart_data:
        abort(404, description="Missing argument time")

    if not isinstance(cart_data['time'], str):
        abort(400, description=f"time = {cart_data['time']} is not string")

    if cart_data['time'] == "":
        abort(400, description=f"time = {cart_data['time']} is empty string")

    try:
        order_date_time = dateutil.parser.isoparse(cart_data['time'])
    except Exception as e:
        raise abort(400, description=f"time = {cart_data['time']} failed because {e}")


@app.route('/')
def default():
    return "Welcome to Delivery fee calculator App"


@app.route('/calculate-delivery-fee', methods=['POST'])
def calculate_delivery_fee() -> json:
    # getting the HTTP request containing cart data
    cart_data = request.get_json()

    # Check if the HTTP request contains all the required fields
    validate_cart_data(cart_data)

    # Calculating delivery fee
    delivery_fee = delivery_fee_calculator(cart_data['cart_value'], cart_data['delivery_distance'],
                                           cart_data['amount_of_items'], cart_data['time'])

    # building the return structure
    ret = {"delivery_fee": delivery_fee}

    return jsonify(ret)


app.run(port=5000)
