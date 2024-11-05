from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from organization.models import Branch
from user.models import Customer
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken

if api_settings.BLACKLIST_AFTER_ROTATION:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from user.models import UserBranchLogin


User = get_user_model()

import json

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)

class TokenObtainSerializer1(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_active_account": _("No active account found with the given credentials")
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
        self.fields["branch"] = serializers.CharField()
        self.fields["firebase_token"] = serializers.CharField(required=False)


    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
            "branch": attrs.get("branch", None),
            "firebase_token" : attrs.get("firebase_token", None)

        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        
        branch = attrs.get("branch", None)
        print(branch)
        firebase_token = attrs.get("firebase_token", None)
        self.firebase_token = firebase_token
        self.branch = branch

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
    
class   TokenObtainPairSerializer1(TokenObtainSerializer1):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)



        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class CustomTokenPairSerializer(TokenObtainPairSerializer1):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Include the "branch" from the data passed during token validation
        branch = attrs.get("branch")
        firebase_token = attrs.get("firebase_token")


        if branch:
            data["branch"] = branch
            # data["token"]["branch"] = branch

        if firebase_token:
            data["firebase_token"] = firebase_token
            print(f"This is the user logged in {self.user}")


        return data
    

    def get_token(self, user):
        token = super().get_token(user)
        token["name"] = user.full_name
        groups = []
        for group in user.groups.values_list("name"):
            groups.append(group[0])
        group_str = json.dumps(groups)
        token["role"] = group_str
        # token["branch"] = attrs.get("branch")

        # branch = attrs.get("branch")
        # if branch:
        #     token["branch"] = branch
        branch = self.branch
        try:
            branch_obj = Branch.objects.get(id=branch)
            token["branch"] = branch
        except(ObjectDoesNotExist, ValueError):
            raise serializers.ValidationError("No branch found")
        
        print(f"This is the firebase token {self.firebase_token}")
        try:
            UserBranchLogin.objects.create(branch=branch_obj, user=self.user, device_token=self.firebase_token)
        except Exception as e:
            raise serializers.ValidationError(f"Error creating the UserBranchLogin, {e}")




        return token



class CustomerSerializer(ModelSerializer):
    loyalty_points = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False, required=False)
    class Meta:
        model = Customer
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "created_by",
        ]
        
from user.models import Customerlogin

class CustomerloginSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Customerlogin
        fields = '__all__'
        
    def validate(self, data):
        # username = data.get('username')
        email = data.get('email')

        # Check if the username already exists
        # if username and Customerlogin.objects.filter(username=username).exists():
        #     raise serializers.ValidationError({'username': 'This username is already in use.'})

        # Check if the email already exists
        if email and Customerlogin.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already in use.'})

        return data

class CustomerloginCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)
    google_id = serializers.CharField(required=False)


from django.contrib.auth.hashers import make_password
from user.models import CustomerNormalLogin
class CustomerNormalLoginSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = CustomerNormalLogin
        fields = ['username', 'password', 'customer', 'email']

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        username = validated_data['username']
        email = validated_data['email']

        # if username and Customer.objects.filter(email=username).exists():
        #     raise serializers.ValidationError({'email': 'This email is already in use.'})

        # Check if a customer with the same username (email) exists
        customer, created = Customer.objects.get_or_create(email=username, defaults=customer_data)



        # If not created, update the existing customer with new data
        if not created:
            for key, value in customer_data.items():
                setattr(customer, key, value)
            customer.save()

        # Create or update CustomerNormalLogin
        customer_login = CustomerNormalLogin.objects.create(username=username, customer=customer, email=email)
        customer_login.password = make_password(validated_data['password'])
        customer_login.save()

        return customer_login
    


class CustomerNormalLoginCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField(required=False)

from django.db.models import Q 
class SetNullPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Check if the username exists
        if not CustomerNormalLogin.objects.filter(Q(username=username)|Q(email=username)).exists():
            raise serializers.ValidationError({'username': 'This username does not exist.'})

        # Perform any additional validation logic here

        return data
        
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

# from api.serializers.user import CustomerGuestSerializer

# from rest_framework import serializers
# # from .models import Customer

# class CustomerGuestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         exclude = [
#             "created_at",
#             "updated_at",
#             "status",
#             "is_deleted",
#             "sorting_order",
#             "is_featured",
#             "created_by",
#             "tax_number",
#             "address",
#             "email", 
#             "branch",
#             "loyalty_points"

#         ]

#     def validate_unique(self, attrs):
#         """
#         Check if a customer with the same name and other details already exists.
#         If it does, let it create a new entry with a different ID.
#         """
#         # Extract values for fields from attrs
#         name = attrs.get('name')
#         # tax_number = attrs.get('tax_number', '')
#         # address = attrs.get('address', '')
#         contact_number = attrs.get('contact_number', '')
#         # email = attrs.get('email', '')
#         # branch = attrs.get('branch', None)

#         # Check for existing customers with the same details
#         matching_customers = Customer.objects.filter(
#             name=name,
#             contact_number=contact_number,

#         )

#         # If an existing customer with the same details is found, let the validation pass
#         # This ensures that the unique constraint is not violated
#         if matching_customers.exists():
#             return attrs

#         # If no matching customer is found, let the default unique validation handle it
#         return super().validate_unique(attrs)
    

class CustomerGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "created_by",
            "tax_number",
            "address",
            "email", 
            "branch",
            "loyalty_points"
        ]

    def create(self, validated_data):
        # Extract relevant validated data
        name = validated_data.get('name')
        contact_number = validated_data.get('contact_number')

        # Check if a customer with the same name and contact number already exists
        existing_customer = Customer.objects.filter(name=name, contact_number=contact_number).first()

        # If an existing customer is found, return it
        if existing_customer:
            return existing_customer

        # If no existing customer is found, create a new one
        new_customer = Customer.objects.create(**validated_data)
        return new_customer