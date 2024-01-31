from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# CarModelInline class

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarModelResource(resources.ModelResource):
    class Meta:
        model = CarModel

class CarMakeResource(resources.ModelResource):
    class Meta:
        model = CarMake

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['get_carmake_name','dealerid','carmodel_name','carmodel_type','year']
    list_filter = ['carmake__carmake_name','carmodel_name','carmodel_type','year']
    search_fields = ['carmake__carmake_name','carmodel_name','carmodel_type','year']
    #resource_classes = [CarModelResource]

    def get_carmake_name(self, obj):
        return obj.carmake.carmake_name

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(ImportExportModelAdmin):
    inlines = [CarModelInline]
    list_display = ['carmake_name', 'description']
    list_filter = ['carmake_name']
    search_fields = ['carmake_name', 'description']
    resource_classes = [CarMakeResource]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
