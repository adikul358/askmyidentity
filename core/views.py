from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Vendor, Product, Order
from .serializers import (
    VendorSerializer, ProductSerializer, OrderSerializer, UserRegisterSerializer, MyTokenObtainPairSerializer
)
from .permissions import IsStoreOwner, IsVendorObject, IsStaffAssignedOrOwner

User = get_user_model()

class RegisterViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Superuser sees everything
        if user.is_superuser:
            return Product.objects.all()
        # limit to user's vendor
        return Product.objects.filter(vendor=user.vendor)

    def perform_create(self, serializer):
        # Owner or staff can create but vendor must be set to user's vendor
        serializer.save(vendor=self.request.user.vendor)

    def get_permissions(self):
        # store owners and staff can use Product endpoints
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        # staff & owners see orders for their vendor only
        return Order.objects.filter(vendor=user.vendor)

    def perform_create(self, serializer):
        # Order placement by customer: set customer and vendor
        user = self.request.user
        if user.role != 'customer':
            # allow owner/staff to create orders on behalf of customers if needed
            vendor = user.vendor
            serializer.save(vendor=vendor, customer=user)
        else:
            serializer.save(vendor=user.vendor, customer=user)
