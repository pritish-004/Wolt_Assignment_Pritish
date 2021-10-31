'''
Backend assignment for Wolt Junior Engineer Program 2021.
Created by Pritish Naik.
'''
import math
import dateutil.parser


def delivery_fee_calculator(cart_value, delivery_distance, amount_of_items, ordered_time_string):

    total_delivery_fee = 0
    surcharge_price = 0

    # point 5 The delivery is free if the cart value is more than 100 Euros
    if cart_value < 10000:
        # point 1 If the cart value is less than 10 Euros, charge surcharge
        if cart_value < 1000:
            surcharge_price = 1000 - cart_value

        # point 2 For the first 1000 meters, the delivery charge is 2 Euros.
        if delivery_distance <= 1000:
            delivery_fee = 200
        else:
            # point 2: 1 Euro is charged for every additional 500m of delivery distance.
            delivery_fee = math.ceil(delivery_distance / 500) * 100

        # point 3: If amount of items is 5 or more, additional 50 cents of
        # surcharge fee is charged for each item
        if amount_of_items >= 5:
            surcharge_price += (amount_of_items - 4) * 50

        # Check if time is in proper format
        try:
            order_date_time = dateutil.parser.isoparse(ordered_time_string)
        except Exception as e:
            raise ValueError(f"Time: {ordered_time_string} is not in ISO format") from e

        # Total delivery fee includes the surcharge price
        total_delivery_fee = delivery_fee + surcharge_price

        # On friday rush hours (3 - 7 PM UTC), the delivery fee is multiplied by 1.1x
        if order_date_time.weekday() == 4 and 15 <= order_date_time.hour < 19:
            total_delivery_fee *= 1.1

        # Total delivery fee cannot exceed 15 Euros and return value must be int
        total_delivery_fee = int(min(1500, total_delivery_fee))

    return total_delivery_fee


if __name__ == '__main__':
    print(delivery_fee_calculator(790, 2235, 4, '2021-10-12T13:00:00Z'))
