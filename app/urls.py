from django.urls import path
from app import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('', views.index, name='home'),
    path('products/', views.Products, name='products'),
    path('product/details/<int:id>/', views.Product_details, name="product_details"),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/<str:action>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("cart/",views.cart, name="cart"),
    
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.toggle_wishlist, name='add_to_wishlist'),
    path('wishlist/delete/<int:product_id>/', views.Delete_wishlist, name='delete_from_wishlist'),
    

    path('my_account/', views.MyAccount, name='my_account'),





]