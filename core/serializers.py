from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Vendor, Product, Order, OrderItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact', 'domain']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'vendor']

    def create(self, validated_data):
        if validated_data.get('role') == 'store_owner' and validated_data.get('vendor') is None:
            raise serializers.ValidationError({'vendor': 'Store owner must have a vendor assigned.'})
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'name', 'description', 'price', 'assigned_to']
        read_only_fields = ['vendor']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'vendor', 'customer', 'created_at', 'status', 'assigned_to', 'items', 'total']
        read_only_fields = ['vendor', 'customer', 'created_at']

    def get_total(self, obj):
        return obj.total()

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # vendor & customer should be set by view using request.user and request.user.vendor
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

# Customizing token to include tenant id and role
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add custom claims
        token['role'] = user.role
        token['tenant_id'] = user.vendor.id if user.vendor else None
        return token