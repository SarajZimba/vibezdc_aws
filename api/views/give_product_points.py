# from rest_framework import generics
# from product.models import ProductPoints
# from api.serializers.give_product_points import ProductPointsSerializer

# class ProductPointsList(generics.ListAPIView):
#     queryset = ProductPoints.objects.order_by('points')
#     serializer_class = ProductPointsSerializer

from rest_framework import generics
from product.models import ProductPoints
from api.serializers.give_product_points import ProductPointsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
# from rest_framework.pagination import PageNumberPagination

# class NoPagination(PageNumberPagination):
#     page_size=None

class ProductPointsList(generics.ListAPIView):

    # queryset = ProductPoints.objects.order_by('points')
    serializer_class = ProductPointsSerializer
    # pagination_class = NoPagination


    def get_queryset(self):

        # queryset = ProductPoints.objects.order_by('points')
        queryset = ProductPoints.objects.filter(is_deleted=False).order_by('points')

        print(queryset)
        return queryset

    def get_serializer_context(self):
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("username")
            role = token_data.get("role")
            # You can access other claims as needed

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")

            # Print the branch
            print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        # Get the base context
        context = super(ProductPointsList, self).get_serializer_context()

        # Add your custom context data here
        context['branch'] = branch  # Replace with your actual branch data

        return context

