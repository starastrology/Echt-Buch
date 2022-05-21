from django.db.models import fields
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Zodiac(models.Model):
    sign = models.CharField(max_length=15)
    value = models.IntegerField(primary_key=True)
    html_code = models.CharField(max_length=10, default="")
    unicode_value = models.CharField(max_length=10, default="")
class Location(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    name = fields.CharField(max_length=200)
class Individual(models.Model):
    profile_pic = models.ImageField(upload_to="profile_pics", default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateTimeField()
    place_of_birth = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pob")
    last_seen = models.ForeignKey(Location, default=None, on_delete=models.CASCADE, related_name="last_seen")
    gender = models.CharField(max_length=10, default="Male")
    sun_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="sun_sign")
    moon_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="moon_sign")
    rising_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="rising_sign")
    mercury_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="mercury_sign")
    venus_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="venus_sign")
    mars_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="mars_sign")
    jupiter_sign = models.ForeignKey(Zodiac, on_delete=models.CASCADE, related_name="jupiter_sign")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def compatibility_REST(self):
        return self._compatibility_REST
    
    @compatibility_REST.setter
    def compatibility_REST(self, value):
        self._compatibility_REST = value
    

class Friendship(models.Model):
    ind1 = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="ind1")
    ind2 = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="ind2")
    pending = models.BooleanField(default=True)
class Post(models.Model):
    text = models.TextField(max_length=2000)
    date_time = models.DateTimeField(default=datetime.now)
    from_ind = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="from_ind")
    to_ind = models.ForeignKey(Individual, on_delete=models.CASCADE, related_name="to_ind")
