from django.db import models
from django.contrib.auth.models import User
from our_product.models import Item

import requests


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_payment_confirmed = models.BooleanField(default=False)
    delivery_charge = models.PositiveIntegerField(default=0)

    def get_delivery_price(start_address, end_address, weight):
        # Define the API endpoint
        api_url = "http://127.0.0.1:2702/priceCalculate/"

        # Define the request payload
        payload = {
            "start_address": start_address,
            "end_address": end_address,
            "weight": weight
        }

        try:
            # Send a POST request to the API
            response = requests.post(api_url, json=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the response JSON
                data = response.json()
                # Return the price, defaulting to 0 if not found
                return data.get("price", 0)
        except Exception as e:
            # Handle any exceptions that may occur during the request
            print(f"Error: {e}")
            return 0
