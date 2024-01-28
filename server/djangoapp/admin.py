from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['carmake_name','dealerid','carmodel_name','carmodel_type','year']
    list_filter = ['carmake__carmake_name','carmodel_name','carmodel_type','year']
    search_fields = ['carmake__carmake_name','carmodel_name','carmodel_type','year']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['carmake_name', 'description']
    list_filter = ['carmake_name']
    search_fields = ['carmake_name', 'description']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
