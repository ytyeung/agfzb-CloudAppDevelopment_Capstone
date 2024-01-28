from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    carmake_name = models.CharField(null=False, max_length=255)
    description = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return f"CarMake: {self.carmake_name}, description: {self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(
        CarMake, null=False, on_delete=models.CASCADE, related_name="carmake"
    )
    dealerid = models.IntegerField()
    carmodel_name = models.CharField(max_length=255)
    carmodel_type = models.CharField(
        max_length=20,
        choices=[("SEDAN","Sedan"),("SUV","SUV"),("WAGON","WAGON")],
        default="SEDAN"
    )
    year = models.IntegerField()

    @property
    def carmake_name(self):
        return self.carmake.carmake_name

    def __str__(self):
        return f"CarMake: {self.carmake_name}, CarModel: {self.carmodel_name}, CarType: {self.carmodel_type}, Year: {self.year}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
