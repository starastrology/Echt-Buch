from django.contrib import admin
from .models import Friendship, Individual, Zodiac, Location, Post
admin.site.register(Individual)
admin.site.register(Zodiac)
admin.site.register(Location)
admin.site.register(Friendship)
admin.site.register(Post)
