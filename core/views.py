from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from blog.models import Blog
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.

class HomePageView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()[:4]
        data['blogs'] = Blog.objects.all()[:4]
        
        return data


class ShopPageView(LoginRequiredMixin, ListView):
    template_name = 'shop.html'
    login_url = '/auth/sign-in/'
    model = Product
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category')
        brand_slug = self.request.GET.get('brand')
        price = self.request.GET.get('price')
        size_id = self.request.GET.get('size')

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(desc__icontains=q)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)

        if size_id:
            queryset = queryset.filter(sizes__id=size_id)
            
        if price:
            price = price.split("-")
            if len(price) == 2:
                queryset = queryset.filter(
                    Q(price__gte=int(price[0][0])) | Q(price__lte=int(price[1][0]))
                )
            queryset = queryset.filter(
                price__gte=int(price[0])
            )


        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data['sizes'] = Size.objects.all()
        data['brands'] = Brand.objects.all()
    
        data['selected_category'] = self.request.GET.get('category')
        data['selected_brand'] = self.request.GET.get('brand')
        data['selected_price'] = self.request.GET.get('price')
        data['selected_size'] = self.request.GET.get('size')
        data['search_query'] = self.request.GET.get('q', '')
        return data

class ShopDetailsPageView(LoginRequiredMixin, DetailView):
    template_name = 'shop-details.html'
    login_url = '/auth/sign-in/'
    model = Product
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.filter(category=data['product'].category).exclude(slug=data['product'].slug)[:4]
        data['images'] = data['product'].images.all()
        return data

@login_required
def cartpageview(request):
    items = CartItem.objects.filter(
        Q(user=request.user) & Q(order__isnull=True)
    )

    
    if request.method == "POST":
        product_slug = request.POST.get('product_slug')
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, slug=product_slug)
        if not product or product is None:
            messages.error("Product not found!")
            render(request, template_name='shopping-cart.html', context={'items':items})
        if product.quantity < quantity:
            messages.error("Product qunatity is not like the quantity you are giving!")
            render(request, template_name='shopping-cart.html', context={'items':items})
        item = CartItem.objects.create(
            user = request.user,
            product = product,
            size = size,
            quantity = quantity,
            order = None
        )
        product.quantity -= quantity
        product.save()
        item.save()
        items = CartItem.objects.filter(
            Q(user=request.user) & Q(order__isnull=True)
        )
        
        render(request, template_name='shopping-cart.html', context={'items':items})
        
    
    return render(request, template_name='shopping-cart.html', context={'items':items})

@login_required
def cartupdateview(request):
    items = CartItem.objects.filter(
        Q(user=request.user) & Q(order__isnull=True)
    )
    
    if request.method == "POST":
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken':
                try:
                    item_id = int(key)
                    new_quantity = int(value)
                except ValueError:
                    continue  

                item = get_object_or_404(CartItem, id=item_id, user=request.user, order=None)
                product = item.product

                diff = new_quantity - item.quantity
                product.quantity -= diff
                item.quantity = new_quantity

                item.save()
                product.save()
        
        items = CartItem.objects.filter(
            Q(user=request.user) & Q(order__isnull=True)
        )
        return render(request, template_name='shopping-cart.html', context={'items': items})

    return render(request, template_name='shopping-cart.html', context={'items': items})


@login_required
def cartdeleteview(request, id):
    item = get_object_or_404(CartItem, id=id, user=request.user, order=None)
    
    if not item:
        messages.error(request, "Item not found!")
    
    product = item.product

    product.quantity += item.quantity
    product.save()
    item.delete()

    items = CartItem.objects.filter(
        Q(user=request.user) & Q(order__isnull=True)
    )
    return render(request, template_name='shopping-cart.html', context={'items': items})

@login_required
def checkoutview(request):
    
    items = CartItem.objects.filter(user=request.user, order=None)
    sub_price = sum(item.total_price for item in items)

    tax = sub_price * Decimal("0.05")
    service_fee = sub_price * Decimal("0.01")

    total_price = sub_price + tax + service_fee
    
    if request.method == "POST":
        ids = request.POST.getlist("cart_items")
        
        items = []
        
        for id_str in ids:
            try:
                id = int(id_str)
            except ValueError:
                continue
                
            try:
                item = CartItem.objects.get(user=request.user, id=id, order=None)
            except CartItem.DoesNotExist:
                messages.error(request, "Some items don’t belong to you or do not exist!")
                return render(request, template_name="checkout.html")
            
            items.append(item)
            
        sub_price = sum(item.total_price for item in items)

        tax = sub_price * Decimal("0.05")
        service_fee = sub_price * Decimal("0.01")

        total_price = sub_price + tax + service_fee

        
        return render(request, template_name="checkout.html", context={"items": items, "sub_price":sub_price, "total_price":total_price})
    
    return render(request, template_name="checkout.html", context={"items": items, "sub_price":sub_price, "total_price":total_price})

@login_required
def create_order(request):
    if request.method != "POST":
        return redirect("core:cart")


    country = request.POST.get("country")
    address = request.POST.get("address")
    town = request.POST.get("town")
    postcode = request.POST.get("postcode")
    notes = request.POST.get("order_notes")
    payment_method = request.POST.get("payment_method")

    cart_item_ids = request.POST.getlist("cart_items")

    if not cart_item_ids:
        messages.error(request, "Cart is empty")
        return redirect("core:cart")
    
    cart_items = CartItem.objects.filter(
        id__in=cart_item_ids,
        user=request.user,
        order__isnull=True
    )

    if not cart_items.exists():
        messages.error(request, "Invalid cart items")
        return redirect("core:cart")
    
    
    subtotal = sum([Decimal(item.total_price) for item in cart_items])
    tax = subtotal * Decimal('0.01')
    shipping = subtotal * Decimal('0.05')
    total = subtotal + tax + shipping


    order = Order.objects.create(
        user=request.user,
        country=country,
        address=address,
        town=town,
        postcode=int(postcode),
        notes=notes,
        subtotal_price=subtotal,
        status="pending",
        payment_model = payment_method
    )

    cart_items.update(order=order)
    messages.success(request, "Order successfully created!")

    return redirect("core:home")

@login_required
def deleteorder(request, id):
    if not request.method == "POST":
        return redirect("/")
    
    order = get_object_or_404(Order, id=id)
    items = CartItem.objects.filter(order = order)
    for item in items:
        product = get_object_or_404(Product, slug = item.product.slug)
        product.quantity += item.quantity
        product.save()
        item.quantity = 0
        item.save()
        
    order.status = 'canceled'
    order.save()
    
    
    return redirect("/")


def orderview(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order.html", {"orders":orders})

class OrderView(LoginRequiredMixin, ListView):
    template_name = "order.html"
    model = Order
    context_object_name = 'orders'
    login_url = '/auth/sign-in/'
    

class AboutPageView(LoginRequiredMixin, TemplateView):
    template_name = 'about.html'
    login_url = '/auth/sign-in/'

class ContactPageView(LoginRequiredMixin, TemplateView):
    template_name = 'contact.html'
    login_url = '/auth/sign-in/'
