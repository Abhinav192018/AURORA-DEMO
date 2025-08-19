from django.shortcuts import render,get_object_or_404,redirect
from app.models import Product,Cart,CartItem,Address,Category,Type,Color,Wishlist

# Create your views here.
from django.contrib.auth.decorators import login_required

def login_view(request):
    next_url = request.GET.get('next', '/')
    return render(request, 'main_page/login.html', {'next': next_url})

def base(request):
    category = Category.objects.all()
    
    context = {
        'category': category,
    }
    return render(request, 'base.html', context)

def index(request):
    category=Category.objects.all()
    products= Product.objects.all().order_by('-id')[:14]
    

    context={
        'category': category,
        'products': products
    }
    return render(request, 'main_page/index.html',context)




from django.db.models import Q
@login_required
def Products(request):

    query=request.GET.get('q')
    type_name=request.GET.get('type')
    wear_type=request.GET.get('wear')
    gift_name=request.GET.get('gift')
    show_latest = request.GET.get('new')
    category_filter = request.GET.get('category')
    price_filter = request.GET.get('price')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products=Product.objects.order_by('-id')

    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)


    if price_filter:
        if price_filter.isdigit():
            products = products.filter(discount_price__lte=int(price_filter))
        elif price_filter == "premium":
            products = products.filter(discount_price__gt=899)
        
    if category_filter:
        products = products.filter(category_obj__name__iexact=category_filter)

    if show_latest:
        products = products[:12]

    if gift_name:
        products=products.filter(gift_obj__name__iexact=gift_name)

    if type_name:
        products=products.filter(type_obj__name__iexact=type_name)

    if wear_type:
        products=products.filter(wear__iexact=wear_type)

    if query:
        products=products.filter(
            Q(name__icontains=query)|
            Q(category_obj__name__icontains=query)|
            Q(type_obj__name__icontains=query)
        ).distinct()


    if min_price:
        products=products.filter(discount_price__gte=min_price)

    if max_price:
        products=products.filter(discount_price__lte=max_price)


    context = {
        'products':products,
        'selected_type':type_name,
        'selected_wear':wear_type,
        'selected_gift':gift_name,
        'search_query':query,
        'min_price': min_price,
        'max_price': max_price,
        'wishlist_ids': wishlist_ids,
    }
    return render(request, 'main_page/products.html', context)



def Product_details(request, id):
    product=get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
        type_obj=product.type_obj
    ).exclude(id=product.id)[:6]

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'main_page/product_details.html', context)


@login_required
def my_orders(request):
    return render(request, 'main_page/my_orders.html')



from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Updated quantity of '{product.name}' in your cart.")
    else:
        messages.success(request, f"'{product.name}' has been added to your cart.")

    return HttpResponseRedirect(reverse('products'))


@login_required
def update_cart_quantity(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
        messages.info(request, f"Increased quantity of '{cart_item.product.name}'.")
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        messages.info(request, f"Decreased quantity of '{cart_item.product.name}'.")
    cart_item.save()

    return HttpResponseRedirect(reverse('cart'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.warning(request,f"Removed '{cart_item.product.name}' from your cart.")
    return HttpResponseRedirect(reverse('cart'))

@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.select_related('product').filter(product__stock__gt=0)

    original_total = sum(item.total_price() for item in items)
    discounted_total = sum(item.discounted_total() for item in items)
    discount_amount = original_total - discounted_total

    context = {
        'items': items,
        'original_total': original_total,
        'discounted_total': discounted_total,
        'discount_amount': discount_amount
    }
    return render(request, 'main_page/cart.html', context)


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()  # Remove if already in wishlist
    else:
        Wishlist.objects.create(user=request.user, product=product)  # Add if not

    return redirect(request.META.get('HTTP_REFERER', 'products'))  # Go back to previous page

@login_required
def Delete_wishlist(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    Wishlist.objects.filter(user=request.user,product=product).delete()
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'main_page/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
def MyAccount(request):
    user = request.user
    profile_pic = None
    google_id = None
    locale = None
    google_profile = None
    name = user.get_full_name() or user.username
    if user.social_auth.exists():
        social = user.social_auth.get(provider='google-oauth2')
        extra = social.extra_data
        profile_pic = extra.get('picture')
        google_id = social.uid
        locale = extra.get('locale')
        google_profile = extra.get('profile')
        name = extra.get('name', name)
    context = {
        'email': user.email,
        'profile_pic': profile_pic,
        'google_id': google_id,
        'locale': locale,
        'google_profile': google_profile,
        'name': name,
    }
    return render(request, 'main_page/my_account.html', context)


