from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from . import forms
from django.conf import settings
from django.conf.urls.static import static
urlpatterns =[
    path('',views.index,name='index'),
    path('about/',views.About,name='about'),
    path('contact/',views.Contact,name='contact'),
    path('shop/',views.Shop,name='shop'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=forms.LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('success/', views.success, name='success'),  
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'product.views.error_404_view'  # Replace with your actual view function
handler500 = 'product.views.error_500_view' 