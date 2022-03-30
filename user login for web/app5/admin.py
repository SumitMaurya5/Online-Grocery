from django.contrib import admin
from .models import Registeration,Customer,Category,Products,Cart,CartProduct

admin.site.register([Registeration,Customer,Category,Products,Cart,CartProduct])