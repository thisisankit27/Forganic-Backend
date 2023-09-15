from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ItemDimensionsSerializer
from rest_framework import status

# from geopy.distance import geodesic

# def calculate_distance(self, start_address, end_address):
#         # Use Geopy to calculate the distance between the addresses
#         start_location = (0, 0)  # Replace with actual coordinates or use a geocoding service
#         end_location = (0, 0)  # Replace with actual coordinates or use a geocoding service

#         # Calculate the distance in kilometers
#         distance = geodesic(start_location, end_location).kilometers

#         return distance

def calculate_distance(start_address, end_address):
        # Implement your logic to calculate the distance between addresses here
        # You may use external services or libraries for this purpose
        # For simplicity, we assume a fixed distance of 10 units here
    return 10

class ItemDimensionsView(APIView):
    def post(self, request):
        # Deserialize the request data using the ItemDimensionsSerializer
        serializer = ItemDimensionsSerializer(data=request.data)

        if serializer.is_valid():
            # Retrieve data from the serializer
            start_address = serializer.validated_data['start_address']
            end_address = serializer.validated_data['end_address']
            weight = serializer.validated_data['weight']

            # Calculate the price based on your business logic
            # Here, we assume a simple example where price = distance * weight
            # You should replace this with your actual pricing logic
            distance = calculate_distance(start_address, end_address)
            price = distance * weight

            # Return the calculated price in the response
            return Response({'price': price}, status=status.HTTP_200_OK)
        else:
            # Return validation errors if the serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

