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
        return f"{self.carmake_name}"


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
        return f"{self.carmake_name} - {self.carmodel_name} - {self.year}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, 
                 purchase_date, car_make, car_model, car_year,
                 sentiment,id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    def __str__(self):
        return f"Dealer name: {self.dealership} Reviewer Name: {self.name} Review: {self.review}"
