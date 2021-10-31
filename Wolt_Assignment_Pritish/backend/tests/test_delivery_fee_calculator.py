import pytest
import requests
from backend.delivery_fee.delivery_fee_calculator import delivery_fee_calculator
import json

BASE_URL = 'http://127.0.0.1:5000/calculate-delivery-fee'
mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def create_request_json(cart_value, delivery_distance, amount_of_items, time):
    return { "cart_value": cart_value, "delivery_distance": delivery_distance, \
             "amount_of_items": amount_of_items, "time": time }


def test_delivery_fee_calculator_function():
    # Wolt example test case
    assert delivery_fee_calculator(790, 2235, 4, '2021-10-12T13:00:00Z') == 710


def test_Wolt_example():

    # Test example test case
    request_json = create_request_json(cart_value=790,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 710

def test_invalid_request_paramaters():

    # Cart value is not integer
    request_json = create_request_json(cart_value="790",delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Delivery distance is not integer
    request_json = create_request_json(cart_value=790,delivery_distance="2235",amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Amount of items is not integer
    request_json = create_request_json(cart_value=790,delivery_distance=2235,amount_of_items="4",time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Time is not string
    request_json = create_request_json(cart_value=790,delivery_distance=2235,amount_of_items=4,time=2021)
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Cart value is not positive integer
    request_json = create_request_json(cart_value=-1,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Delivery distance is not positive integer
    request_json = create_request_json(cart_value=790,delivery_distance=-20,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Amount of items is not positive integer
    request_json = create_request_json(cart_value=790,delivery_distance=2235,amount_of_items=-4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Cart value is Zero
    request_json = create_request_json(cart_value=0,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Delivery distance is Zero
    request_json = create_request_json(cart_value=790,delivery_distance=0,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Amount of items is Zero
    request_json = create_request_json(cart_value=790,delivery_distance=2235,amount_of_items=0,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Time is an empty string
    request_json = create_request_json(cart_value=790,delivery_distance="2235",amount_of_items=4,time="")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Time is not in ISO format
    request_json = create_request_json(cart_value=790,delivery_distance="2235",amount_of_items=4,time="2021-")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

    # Time is incorrect
    request_json = create_request_json(cart_value=790,delivery_distance="2235",amount_of_items=4,time="2021-10-12T25:21:21Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 400

def test_request_missing_parameters():

    # Cart value parameter is missing
    request_json = { "delivery_distance": 2235, "amount_of_items": 4, "time": "2021-10-12T13:00:00Z" }
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 404

    # delivery distance parameter is missing
    request_json = { "cart_value": 790, "amount_of_items": 4, "time": "2021-10-12T13:00:00Z" }
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 404

    # Amount of items parameter is missing
    request_json = { "cart_value": 790, "delivery_distance": 2235 , "time": "2021-10-12T13:00:00Z" }
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 404

    # Time parameter is missing
    request_json = { "cart_value": 790, "delivery_distance": 2235, "amount_of_items": 4 }
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    assert response.status_code == 404

def test_delivery_fee():

    # Delivery is free if cart value is equal or more than 100 Euros
    request_json = create_request_json(cart_value=10000,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 0

    # Delivery is free if cart value is equal or more than 100 Euros
    request_json = create_request_json(cart_value=23425,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 0

    # Delivery is free if cart value is equal or more than 100 Euros
    request_json = create_request_json(cart_value=23425,delivery_distance=2235,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 0

    # Surcharge fee is charged if cart value is less than 10 Euros
    # Calculation: delivery fee = 900(surcharge) + 500(distance fee) + 50(surcharge (>4 items)) = 1450 cents
    request_json = create_request_json(cart_value=100,delivery_distance=2235,amount_of_items=5,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 1450

    # Surcharge fee is charged if cart value is less than 10 Euros
    # Calculation: delivery fee = 900(surcharge) + 500(distance fee) + 50(surcharge (>4 items)) = 1450 cents
    request_json = create_request_json(cart_value=100,delivery_distance=2235,amount_of_items=5,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 1450

    # Delivery fee if delivery distance is less than 1000 meters(1Km)
    # Calculation: delivery fee =  200(distance fee) = 200 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=99,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 200

    # Delivery fee if delivery distance is 1001 meters
    # Calculation: delivery fee =  300(distance fee) = 300 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=1001,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300

    # Delivery fee if delivery distance is 1499 meters
    # Calculation: delivery fee =  300(distance fee) = 300 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=1001,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300

    # Delivery fee if delivery distance is 1500 meters
    # Calculation: delivery fee =  300(distance fee) = 300 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=1500,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300

    # Delivery fee if delivery distance is 1501 meters
    # Calculation: delivery fee =  400(distance fee) = 400 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=1501,amount_of_items=4,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 400

    # Surcharge fee is charged for each item above 5
    # Calculation: delivery fee =  200(distance fee) + 100(surcharge (>4 items)) = 300 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=99,amount_of_items=6,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300

    # Surcharge fee is charged for each item above 5
    # Calculation: delivery fee =  200(distance fee) + 100(surcharge (>4 items)) = 300 cents
    request_json = create_request_json(cart_value=1000,delivery_distance=99,amount_of_items=6,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300

    # Delivery fee can never be more than 15 Euros (1500 cents)
    # Calculation: delivery fee =  900(surcharge) + 2000(distance fee) + 100(surcharge (>4 items)) = 3000 cents
    # Delivery fee is capped on (15 Euros)
    request_json = create_request_json(cart_value=100,delivery_distance=1000000,amount_of_items=6,time="2021-10-12T13:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 1500 # 15 Euros

def test_friday_rush_hours():
    # Friday rush ( 3 - 7 PM UTC), the delivery fee will be multiplied by 1.1x
    # Delivery fee can never be more than 15 Euros (1500 cents)
    # Calculation: delivery fee = [200(distance fee) + 100(surcharge (>4 items))] x 1.1 = 300 x 1.1 = 330
    request_json = create_request_json(cart_value=1000,delivery_distance=1000,amount_of_items=6,time="2021-10-22T15:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 330 # 3.3 Euros

    # Friday rush ( 3 - 7 PM UTC), the delivery fee will be multiplied by 1.1x
    # The rush hours end at exact 7PM, so no rush hours multiplication at 7PM
    # Calculation: delivery fee = [200(distance fee) + 100(surcharge (>4 items))] = 300
    request_json = create_request_json(cart_value=1000,delivery_distance=1000,amount_of_items=6,time="2021-10-22T19:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 300 # 3 Euros

    # Friday rush ( 3 - 7 PM UTC), the delivery fee will be multiplied by 1.1x
    # Delivery fee can never be more than 15 Euros (1500 cents)
    # Calculation: delivery fee = [200(distance fee) + 100(surcharge (>4 items))] x 1.1 = 300 x 1.1 = 330 
    request_json = create_request_json(cart_value=1000,delivery_distance=1000,amount_of_items=6,time="2021-10-22T18:59:59Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 330 # 3.3 Euros


    # Friday rush ( 3 - 7 PM UTC), the delivery fee will be multiplied by 1.1x
    # Delivery fee can never be more than 15 Euros (1500 cents)
    # Calculation: delivery fee = [900(surcharge) + 300(distance fee) + 100(surcharge (>4 items))] x 1.1 = 1300 x 1.1 = 1430
    request_json = create_request_json(cart_value=100,delivery_distance=1500,amount_of_items=6,time="2021-10-22T15:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 1430 # 14.3 Euros

    # Friday rush ( 3 - 7 PM UTC), the delivery fee will be multiplied by 1.1x
    # Delivery fee can never be more than 15 Euros (1500 cents)
    # Calculation: delivery fee = [900(surcharge) + 400(distance fee) + 100(surcharge (>4 items))] x 1.1 = 1400 x 1.1 = 1540
    # The delivery fee is capped at 1500 cents
    request_json = create_request_json(cart_value=100,delivery_distance=2000,amount_of_items=6,time="2021-10-22T15:00:00Z")
    response = requests.post(BASE_URL, data=json.dumps(request_json), headers=headers)
    result = response.json()
    assert response.status_code == 200
    assert result['delivery_fee'] == 1500 # 15 Euros
