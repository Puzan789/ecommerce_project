from django.urls import path
from .import views
urlpatterns =[
    path('',views.index,name='index'),
    path('about/',views.About,name='about'),
    path('contact/',views.Contact,name='contact'),
    path('shop/',views.Shop,name='shop'),
]