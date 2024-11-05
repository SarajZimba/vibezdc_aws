

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from user.models import Customer
from ..serializers.user import CustomTokenPairSerializer,CustomerNormalLoginCreateSerializer, CustomerSerializer, CustomerloginSerializer,CustomerloginCheckSerializer, CustomerNormalLoginSerializer, PasswordResetSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]  # If you want to keep these authentication classes
    permission_classes = [AllowAny]  # Excludes authentication for this view

class CustomerAPI(ModelViewSet):
    serializer_class = CustomerSerializer
    model = Customer
    queryset = Customer.objects.active()
    pagination_class = None

    # Allow only patch requests
    http_method_names = ['get', 'post', 'head', 'options', 'patch']

    def perform_update(self, serializer):
        # Update only the fields that are provided in the request data
        serializer.save()

from user.models import Customerlogin


class CustomerloginViewSet(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Customerlogin.objects.all()
    serializer_class = CustomerloginSerializer

    def create(self, request, *args, **kwargs):
        # Extract customer data from the request
        customer_data = request.data.pop('customer', None)

        # Serialize customer data
        customer_serializer = CustomerSerializer(data=customer_data)

        customer_serializer.is_valid(raise_exception=True)

        # Create customer instance
        # customer_instance, _ = Customer.objects.get_or_create(**customer_serializer.validated_data)
        email = request.data.get('email')
        print(email)
        customer, created = Customer.objects.get_or_create(email=email, defaults=customer_data)



        # If not created, update the existing customer with new data
        if not created:
            for key, value in customer_data.items():
                setattr(customer, key, value)
            customer.save()

        # Include the customer instance in the request data
        request.data['customer'] = customer_serializer.data

        # Continue with the rest of the creation process using the original serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set password and perform the rest of the creation process
        password = request.data.get('password')
        serializer.validated_data['password'] = password
        instance = serializer.save(customer=customer)

        # Set password for the instance
        instance.set_password(password)
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        # Set password and perform the rest of the update process
        password = self.request.data.get('password')
        serializer.validated_data['password'] = password
        instance = serializer.save()

        # Set password for the instance
        instance.set_password(password)
        instance.save()

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import Customerlogin,CustomerNormalLogin

class CustomerloginCheckView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = CustomerloginCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data.get('password')
        google_id = serializer.validated_data.get('google_id')

        queryset = Customerlogin.objects.filter(email=email)

        if google_id:
            queryset = queryset.filter(google_id=google_id)

        if password:
            queryset = queryset.filter(password=password)

        if not queryset.exists():
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        customerlogin_instance = queryset.first()
        customer_serializer = CustomerSerializer(customerlogin_instance.customer)
        return Response({'customer': customer_serializer.data}, status=status.HTTP_200_OK)
    
    # views.py
from rest_framework import generics

class CustomerNormalLoginCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomerNormalLogin.objects.all()
    serializer_class = CustomerNormalLoginSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



from django.contrib.auth.hashers import check_password
from django.db.models import Q

class CustomerLoginAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = CustomerNormalLoginCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        try:
            # customer_login = CustomerNormalLogin.objects.get(username=username)
            customer_login = CustomerNormalLogin.objects.get(Q(username=username)|Q(email=username))
            if customer_login.password is None:
                return Response({'is_null':True}, status=status.HTTP_404_NOT_FOUND)
        except CustomerNormalLogin.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, customer_login.password):
            # Passwords match, return customer details
            response_data = {'customer' : {
                'username': customer_login.username,
                'email': customer_login.email,
                'id': customer_login.customer.id,
                'name': customer_login.customer.name,
                'email': customer_login.customer.email,
                'contact_number': customer_login.customer.contact_number,
                # Add any other customer details you want to include
            }}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
from django.contrib.auth.hashers import make_password
from api.serializers.user import SetNullPasswordSerializer

class SetNullPasswordView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = CustomerNormalLogin.objects.all()
    serializer_class = SetNullPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the username and password from the validated data
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(username)

        # Update the password for instances where the password is currently None
        # instances_with_null_password = CustomerNormalLogin.objects.filter(username=username, password=None)
        # for instance in instances_with_null_password:
        #     instance.password = make_password(password)
        #     instance.save()
            
        # customer = instances_with_null_password.customer
        # instance = CustomerNormalLogin.objects.filter(username=username, password=None).first()
        instance = CustomerNormalLogin.objects.filter((Q(username=username)|Q(email=username)) & Q(password=None)).first()




        instance.password = make_password(password)
        instance.save()

        customer = instance.customer
        response_data = {
            'customer': {
                'name': customer.name,
                'email':customer.email,
                'id': customer.id,
                'name': customer.name, 
                'email': customer.email, 
                'contact_no': customer.contact_number,
            }            
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED)

from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import timedelta

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                # user = CustomerNormalLogin.objects.get(email=email)
                user = CustomerNormalLogin.objects.get(Q(username=email)|Q(email=email))

            except CustomerNormalLogin.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Generate and save a reset token and expiry date
            user.reset_token = uuid.uuid4().hex  # Convert UUID to a string
            user.reset_token_expiry = timezone.now() + timedelta(hours=1)
            user.save()

            # Send email with the reset link
            reset_link = f"{settings.FRONTEND_URL}/password-reset/{user.reset_token}/"
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )

            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
from django.shortcuts import get_object_or_404

class PasswordResetConfirmView(APIView):
    def post(self, request, reset_token, *args, **kwargs):
        # Use get_object_or_404 to handle the case where the user is not found
        user = get_object_or_404(CustomerNormalLogin, reset_token=reset_token)

        # Check if the token is still valid
        if user.reset_token_expiry > timezone.now():
            new_password = request.data.get('new_password')
            user.password = make_password(new_password)
            # user.reset_token = None
            # user.reset_token_expiry = None
            user.save()

            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
            
from api.serializers.user import CustomerGuestSerializer

class CreateGuestCustomerView(APIView):
    
    def post(self, request, format=None):
        serializer = CustomerGuestSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            response_data = {
                'customer': {
                    'name': customer.name,
                    'email':customer.email,
                    'id': customer.id,
                    'name': customer.name, 
                    'email': customer.email, 
                    'contact_number': customer.contact_number,
                }            
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

