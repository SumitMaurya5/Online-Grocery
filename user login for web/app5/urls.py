from .views import login,mainPage,category,productview,category,categorywise,logout,AddtoCartView,ManageCartView,EmptyCartView, search
from .views import MyCartView,contact
from django.urls import path

urlpatterns = [
    path('login/',login,name = 'login'),
    path('',mainPage,name = 'main'),
    path('category/',category,name = 'category'),
    path("product/<str:title>/",productview,name="prodetails"),
    path('categorywise/<str:title>/',categorywise),
    path('logout/',logout,name='logout'),
    path("add_to_cart-<int:pro_id>/",AddtoCartView.as_view(), name="addtocart"),
    path("my_cart/",MyCartView.as_view(), name="mycart"),
    path("manage_cart/<int:cp_id>/",ManageCartView.as_view(), name="managecart"),
    path("empty_cart/",EmptyCartView.as_view(), name="emptycart"),
    path('contact/',contact,name='contact'),
    path('search/',search,name='search'),
    # path('Cuopan_apply/', Cuopan_apply, name="Cuopan_apply"),
]