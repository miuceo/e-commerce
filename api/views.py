from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action
from rest_framework import mixins, viewsets, permissions, status, serializers, exceptions

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from authentication.models import CustomUser
from authentication.models import CustomUser
from blog.models import Blog, Tag
from core.models import (Category,
                         Brand,
                         Size,
                         ProductImages,
                         Product,
                         CartItem,
                         Order)

from .serializers import CustomTokenObtainSerializer, AddToCartSerializer
from authentication.serializers import CustomUserSerializer
from blog.serializers import BlogSerializer, TagSerializer
from core.serializers import (CategorySerializer,
                              BrandSerializer,
                              SizeSerializer,
                              ProductImagesSerializer,
                              ProductSerializer,
                              CartItemSerializer,
                              OrderSerializer,
                              OrderCreateSerializer)

# Create your views here.

# Permissions
    
class RegisterUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (not request.user) and not (request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class AdminUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

class CustomPermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
        
class SellerProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'seller' or request.user.role == "admin")
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        
slug_param = [
    OpenApiParameter(
        name="slug",
        description="Slug of the product",
        required=True,
        type=str,
        location=OpenApiParameter.PATH
    )
]        
        
# Views

@extend_schema_view(
    list=extend_schema(
        summary="List all users (Admin only)",
        description="Returns a list of all users. Accessible only to admin users.",
        tags=["Admin Users"],
    ),
    retrieve=extend_schema(
        summary="Retrieve user details (Admin only)",
        tags=["Admin Users"],
    ),
    create=extend_schema(
        summary="Create a new user (Admin only)",
        tags=["Admin Users"],
    ),
    update=extend_schema(
        summary="Update user (Admin only)",
        tags=["Admin Users"],
    ),
    partial_update=extend_schema(
        summary="Partially update user (Admin only)",
        tags=["Admin Users"],
    ),
    destroy=extend_schema(
        summary="Delete user (Admin only)",
        tags=["Admin Users"],
    ),
)
class AdminUsersView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated, AdminUserPermission]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
@extend_schema_view(
    list=extend_schema(
        summary="List all blogs (Admin only)",
        description="Returns a list of all blogs. Accessible only to admin users.",
        tags=["Admin Blogs"],
    ),
    retrieve=extend_schema(
        summary="Retrieve blog details by slug (Admin only)",
        tags=["Admin Blogs"],
    ),
    create=extend_schema(
        summary="Create a new blog (Admin only)",
        tags=["Admin Blogs"],
    ),
    update=extend_schema(
        summary="Update blog by slug (Admin only)",
        tags=["Admin Blogs"],
    ),
    partial_update=extend_schema(
        summary="Partially update blog by slug (Admin only)",
        tags=["Admin Blogs"],
    ),
    destroy=extend_schema(
        summary="Delete blog by slug (Admin only)",
        tags=["Admin Blogs"],
    ),
)
class AdminBlogView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        AdminUserPermission,
    ]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "slug"
    

@extend_schema_view(
    list=extend_schema(
        summary="List all tags (Admin only)",
        description="Returns a list of all tags. Accessible only to admin users.",
        tags=["Admin Tags"],
    ),
    retrieve=extend_schema(
        summary="Retrieve tag details by ID (Admin only)",
        tags=["Admin Tags"],
    ),
    create=extend_schema(
        summary="Create a new tag (Admin only)",
        tags=["Admin Tags"],
    ),
    update=extend_schema(
        summary="Update tag by ID (Admin only)",
        tags=["Admin Tags"],
    ),
    partial_update=extend_schema(
        summary="Partially update tag by ID (Admin only)",
        tags=["Admin Tags"],
    ),
    destroy=extend_schema(
        summary="Delete tag by ID (Admin only)",
        tags=["Admin Tags"],
    ),
)
class AdminTagView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        AdminUserPermission,
    ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    
@extend_schema_view(
    list=extend_schema(
        summary="List all categories (Admin only)",
        description="Returns a list of all categories. Accessible only to admin users.",
        tags=["Admin Categories"],
    ),
    retrieve=extend_schema(
        summary="Retrieve category details by slug (Admin only)",
        tags=["Admin Categories"],
    ),
    create=extend_schema(
        summary="Create a new category (Admin only)",
        tags=["Admin Categories"],
    ),
    update=extend_schema(
        summary="Update category by slug (Admin only)",
        tags=["Admin Categories"],
    ),
    partial_update=extend_schema(
        summary="Partially update category by slug (Admin only)",
        tags=["Admin Categories"],
    ),
    destroy=extend_schema(
        summary="Delete category by slug (Admin only)",
        tags=["Admin Categories"],
    ),
)
class AdminCategoryView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        AdminUserPermission,
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    

@extend_schema_view(
    list=extend_schema(
        summary="List all brands (Admin only)",
        description="Returns a list of all brands. Accessible only to admin users.",
        tags=["Admin Brands"],
    ),
    retrieve=extend_schema(
        summary="Retrieve brand details by slug (Admin only)",
        tags=["Admin Brands"],
    ),
    create=extend_schema(
        summary="Create a new brand (Admin only)",
        tags=["Admin Brands"],
    ),
    update=extend_schema(
        summary="Update brand by slug (Admin only)",
        tags=["Admin Brands"],
    ),
    partial_update=extend_schema(
        summary="Partially update brand by slug (Admin only)",
        tags=["Admin Brands"],
    ),
    destroy=extend_schema(
        summary="Delete brand by slug (Admin only)",
        tags=["Admin Brands"],
    ),
)
class AdminBrandView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        AdminUserPermission,
    ]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "slug"
    
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
    
@extend_schema_view(
    create=extend_schema(
        summary="Create a new user",
        tags=["Ordinary Users"],
    ),
    update=extend_schema(
        summary="Update user",
        tags=["Ordinary Users"],
    ),
    partial_update=extend_schema(
        summary="Partial update user",
        tags=["Ordinary Users"],
    ),
)
class UserRegister(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class HomePageView(APIView):
    permission_classes = [CustomPermisson]
    
    @extend_schema(
        summary="Homepage endpoint",
        description="Simple authenticated endpoint returning a welcome message.",
        responses={200: dict},
        tags=["Public"],
    )
    def get(self, request):
        return Response(
            {"message": "Hello world!"},
            status=status.HTTP_200_OK,
        )
        
        
@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Returns a list of all products. Accessible only to all users.",
        tags=["All products"],
    ),
    retrieve=extend_schema(
        summary="Retrieve product details by slug",
        tags=["All products"],
        parameters=slug_param,
        responses=ProductSerializer
    ),
)
class ProductsView(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    
    permission_classes = [CustomPermisson]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug" 
    
    def retrieve(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        pr_ser = ProductSerializer(product)
        return Response(
            status=status.HTTP_200_OK,
            data=pr_ser.data
        )
        
    @extend_schema(
        summary="Add product to cart",
        tags=["All products"],
        parameters=slug_param,
        request=AddToCartSerializer,
        responses=ProductSerializer
    )
    @action(detail=True, methods=['post'])
    def add(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer = AddToCartSerializer(data=request.data, context={"product": product})
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]
        size = serializer.validated_data["size"]

        item = CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            size=size,
            order=None
        )

        product.quantity -= quantity
        product.save()

        return Response(
            data=CartItemSerializer(item).data,
            status=200
        )
    

@extend_schema_view(
    list=extend_schema(
        summary="List all sizes (Admin only)",
        description="Returns a list of all sizes. Accessible only to admin users.",
        tags=["Admin Sizes"],
    ),
    retrieve=extend_schema(
        summary="Retrieve size details by ID (Admin only)",
        tags=["Admin Sizes"],
    ),
    create=extend_schema(
        summary="Create a new size (Admin only)",
        tags=["Admin Sizes"],
    ),
    update=extend_schema(
        summary="Update size by ID (Admin only)",
        tags=["Admin Sizes"],
    ),
    partial_update=extend_schema(
        summary="Partially update size by ID (Admin only)",
        tags=["Admin Sizes"],
    ),
    destroy=extend_schema(
        summary="Delete size by ID (Admin only)",
        tags=["Admin Sizes"],
    ),
)
class AdminSizeView(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        AdminUserPermission,
    ]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class SellerProductView(viewsets.ModelViewSet):
    permission_classes = [SellerProductPermission]
    queryset = get_list_or_404(Product)
    serializer_class = ProductSerializer
    lookup_field = "slug"
    
    
    def retrieve(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if (product.seller_id == request.user and request.user.role in ['admin', 'seller']) or request.user.role == "admin": 
            return Response(
                data=ProductSerializer(product).data,
                status=status.HTTP_200_OK
            )
            
        else:
            raise exceptions.APIException(
                detail='You don\'t have permissons!'
            )
            
    def update(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=kwargs["slug"])

        if not (
            request.user.role == "admin"
            or (request.user.role == "seller" and product.seller_id == request.user)
        ):
            raise exceptions.PermissionDenied("You don't have permissions!")

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=request.method == "PATCH"
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

            
    def destroy(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if (product.seller_id == request.user and request.user.role in ['admin', 'seller']) or request.user.role == "admin": 
            product.delete()
            
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Deleted!"}
            )
            
        else:
            raise exceptions.APIException(
                detail='You don\'t have permissons!'
            )
            

class UserCartViews(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(
            user=self.request.user
        )

    def update(self, request, pk=None):
        return self.update_item(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self.update_item(request, pk, partial=True)

    def update_item(self, request, pk, partial):
        cart_item = get_object_or_404(
            CartItem,
            pk=pk,
            user=request.user,
            order__isnull=True
        )

        if "order" in request.data:
            raise exceptions.ValidationError(
                {"order": "Order ni o‘zgartirish mumkin emas"}
            )

        product = cart_item.product

        old_quantity = cart_item.quantity
        old_size = cart_item.size

        new_quantity = request.data.get("quantity", old_quantity)
        new_size = request.data.get("size", old_size)

        try:
            new_quantity = int(new_quantity)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                {"quantity": "Quantity butun son bo‘lishi kerak"}
            )

        if new_quantity <= 0:
            raise exceptions.ValidationError(
                {"quantity": "Quantity 0 dan katta bo‘lishi kerak"}
            )

        if not product.sizes.filter(name=new_size).exists():
            raise exceptions.ValidationError(
                {"size": f"{new_size} bu product uchun mavjud emas"}
            )

        diff = new_quantity - old_quantity

        if diff > 0:
            if product.quantity < diff:
                raise exceptions.ValidationError(
                    {"quantity": "Product stock yetarli emas"}
                )
            product.quantity -= diff

        elif diff < 0:
            product.quantity += abs(diff)

        product.save()

        cart_item.quantity = new_quantity
        cart_item.size = new_size
        cart_item.save()

        return Response(
            self.get_serializer(cart_item).data,
            status=status.HTTP_200_OK
        )
        
class NonOrderCartView(viewsets.ViewSet):
    permission_classes = [CustomPermisson]

    @extend_schema(
        summary="List orders from non-order cart items",
        tags=["Non-order cart items"],
        responses=[CartItemSerializer]
    )
    def list(self, request):
        items = CartItem.objects.filter(
            user=request.user,
            order__isnull=True
        )
        return Response(
            CartItemSerializer(items, many=True).data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Create order from non-order cart items",
        tags=["Non-order cart items"],
        request=OrderCreateSerializer,
        responses=OrderSerializer
    )
    @action(detail=False, methods=["post"])
    def order(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = CartItem.objects.filter(
            user=request.user,
            order__isnull=True
        )

        if not items.exists():
            raise exceptions.ValidationError(
                "Cart bo‘sh, order yaratib bo‘lmaydi"
            )

        subtotal = sum(item.total_price for item in items)

        order = Order.objects.create(
            user=request.user,
            country=serializer.validated_data["country"],
            address=serializer.validated_data["address"],
            town=serializer.validated_data["town"],
            postcode=serializer.validated_data["postcode"],
            notes=serializer.validated_data.get("notes"),
            payment_model=serializer.validated_data["payment_model"],
            subtotal_price=subtotal
        )
        items.update(order=order)
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
        
class OrdersView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="List orders from user orders",
        tags=["Orders"],
        request=OrderCreateSerializer,
        responses=OrderSerializer
    )
    def list(self, request):
        orders = get_list_or_404(Order, user=request.user)
        return Response(
            status=status.HTTP_200_OK,
            data=OrderSerializer(orders, many=True).data
        )
        
    @extend_schema(
        summary="Cancel order",
        tags=["Orders"],
        responses=OrderSerializer
    )
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk):
        order = Order.objects.get(pk=pk, user=request.user)
        if order.status in ['completed', 'cancelled']:
            raise exceptions.APIException(
                detail='This order is already cancelled or completed!'
            )
        
        items = CartItem.objects.filter(user = request.user, order = order)    
        
        for item in items:
            product = Product.objects.get(slug=item.product.slug)
            product.quantity += item.quantity
            item.quantity = 0
            item.save()
            product.save()
            
        order.status = "cancelled"
        order.save()
        
        return Response(
            status=status.HTTP_202_ACCEPTED,
            data=OrderSerializer(order).data
        )