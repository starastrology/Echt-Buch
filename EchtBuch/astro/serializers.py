from django.contrib.auth.models import User
from rest_framework import serializers
from astro.models import Individual, Location, Zodiac, Friendship, Post
from datetime import datetime

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ["latitude", "longitude", "name"]

class ZodiacSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zodiac
        fields = ["value", "sign", "html_code", "unicode_value"]
    
class IndividualSerializer(serializers.HyperlinkedModelSerializer):
    place_of_birth = LocationSerializer()
    sun_sign = ZodiacSerializer()
    moon_sign = ZodiacSerializer()
    rising_sign = ZodiacSerializer()
    mercury_sign = ZodiacSerializer()
    venus_sign = ZodiacSerializer()
    mars_sign = ZodiacSerializer()
    jupiter_sign = ZodiacSerializer()
    user = UserSerializer()
    last_seen = LocationSerializer()
    compatibility_REST = 0.0

    class Meta:
        model = Individual
        fields = ["id", "first_name", "last_name", "user", "dob", "place_of_birth", "last_seen", "gender", "sun_sign", "moon_sign", \
                "rising_sign", "mercury_sign", "venus_sign", "mars_sign", "jupiter_sign", "profile_pic", "compatibility_REST"]



class PostSerializer(serializers.HyperlinkedModelSerializer):
    to_ind = IndividualSerializer()
    from_ind = IndividualSerializer()

    class Meta:
        model = Post
        fields = ["id", "text", "date_time", "to_ind", "from_ind"]



class FriendshipSerializer(serializers.HyperlinkedModelSerializer):
    ind1 = IndividualSerializer()
    ind2 = IndividualSerializer()

    class Meta:
        model = Friendship
        fields = ["ind1", "ind2", "pending"]


