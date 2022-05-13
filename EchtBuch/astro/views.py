from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from astro.models import Friendship, Individual, Zodiac, Location, Post
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login as auth_login
from django.contrib import messages
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
from math import floor
from math import ceil
from datetime import datetime
from datetime import timedelta
import pytz
from tzwhere import tzwhere
import operator
from geopy.geocoders import Nominatim
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from astro.serializers import UserSerializer, IndividualSerializer, LocationSerializer, ZodiacSerializer, PostSerializer, FriendshipSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class= UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class IndividualViewSet(viewsets.ModelViewSet):
    queryset = Individual.objects.all()
    serializer_class= IndividualSerializer
    permission_classes = [permissions.IsAuthenticated]

def friends_list(request):
    username = ""
    if request.GET.get('username'):
        username = request.GET["username"]
    
    u = Individual.objects.get(user__username=username)
    if request.GET.get('friend'):
        friend = request.GET["friend"]
        f = Individual.objects.filter(user__username=friend).first()
        if f:
            friendship = Friendship.objects.filter((Q(ind1=u)|Q(ind2=u))&(Q(ind1=f)|Q(ind2=f)), pending__in=[False]).first()
            if friendship:
                serializer = FriendshipSerializer(friendship, many=False)
                return JsonResponse(serializer.data, safe=True)
            else:
                return JsonResponse({}, safe=True)
        else:
            return JsonResponse({}, safe=True)

    friendships = Friendship.objects.filter((Q(ind1=u)|Q(ind2=u)), pending__in=[False])   
    friends = Individual.objects.none()
    for friendship in friendships:
        if friendship.ind1 == u:
            friends |= Individual.objects.filter(pk=friendship.ind2.id)
        else:
            friends |= Individual.objects.filter(pk=friendship.ind1.id)
    
    for user in friends:
        user.compatibility_REST = 0.0
        if u.sun_sign.value == user.sun_sign.value:
            user.compatibility_REST = 1.5
        else:
            diff = abs(u.sun_sign.value - user.sun_sign.value)
            if diff > 6:
                user.compatibility_REST = (12 - diff) * .25
            else:
                user.compatibility_REST = diff * .25
        if u.moon_sign.value == user.moon_sign.value:
            user.compatibility_REST += 1.2
        else:
            diff = abs(u.moon_sign.value - user.moon_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .2
            else:
                user.compatibility_REST += diff * .2
        if u.rising_sign.value == user.rising_sign.value:
            user.compatibility_REST += .9
        else:
            diff = abs(u.rising_sign.value - user.rising_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .15
            else:
                user.compatibility_REST += diff * .15
        if u.mercury_sign.value == user.mercury_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.mercury_sign.value - user.mercury_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.venus_sign.value == user.venus_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.venus_sign.value - user.venus_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.mars_sign.value == user.mars_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.mars_sign.value - user.mars_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.jupiter_sign.value == user.jupiter_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        user.compatibility_REST = round((user.compatibility_REST - 1) / 5.0 * 100.0, 1)
    friends = sorted(friends, key=operator.attrgetter('compatibility_REST'), reverse=True)
    serializer = IndividualSerializer(friends, many=True)
    return JsonResponse(serializer.data, safe=False)


def friends_pending_list(request):
    username = ""
    if request.GET.get('username'):
        username = request.GET["username"]
    u = Individual.objects.get(user__username=username)
    friendships = Friendship.objects.filter((Q(ind1=u)|Q(ind2=u)), pending__in=[True])   
    
    friends = Individual.objects.none()
    for friendship in friendships:
        if friendship.ind1 == u:
            friends |= Individual.objects.filter(pk=friendship.ind2.id)
        else:
            friends |= Individual.objects.filter(pk=friendship.ind1.id)
    
    for user in friends:
        user.compatibility_REST = 0.0
        if u.sun_sign.value == user.sun_sign.value:
            user.compatibility_REST = 1.5
        else:
            diff = abs(u.sun_sign.value - user.sun_sign.value)
            if diff > 6:
                user.compatibility_REST = (12 - diff) * .25
            else:
                user.compatibility_REST = diff * .25
        if u.moon_sign.value == user.moon_sign.value:
            user.compatibility_REST += 1.2
        else:
            diff = abs(u.moon_sign.value - user.moon_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .2
            else:
                user.compatibility_REST += diff * .2
        if u.rising_sign.value == user.rising_sign.value:
            user.compatibility_REST += .9
        else:
            diff = abs(u.rising_sign.value - user.rising_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .15
            else:
                user.compatibility_REST += diff * .15
        if u.mercury_sign.value == user.mercury_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.mercury_sign.value - user.mercury_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.venus_sign.value == user.venus_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.venus_sign.value - user.venus_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.mars_sign.value == user.mars_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.mars_sign.value - user.mars_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        if u.jupiter_sign.value == user.jupiter_sign.value:
            user.compatibility_REST += .6
        else:
            diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
            if diff > 6:
                user.compatibility_REST += (12 - diff) * .1
            else:
                user.compatibility_REST += diff * .1
        user.compatibility_REST = round((user.compatibility_REST - 1) / 5.0 * 100.0, 1)
    friends = sorted(friends, key=operator.attrgetter('compatibility_REST'), reverse=True)
    serializer = IndividualSerializer(friends, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_comments(request):
    if request.GET.get("username"):
        i = Individual.objects.get(user__username=request.GET['username'])
        comments = Post.objects.filter(to_ind=i).order_by("-date_time")
        serializer = PostSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse([{}], safe=False)



def individual_list(request):
    queryset = Individual.objects.all()    
    if request.GET.get("username"):
        queryset = queryset.exclude(user__username=request.GET["username"])
        u = Individual.objects.get(user__username=request.GET["username"]) 
        for user in queryset:
            user.compatibility_REST = 0.0
            if u.sun_sign.value == user.sun_sign.value:
                 user.compatibility_REST = 1.5
            else:
                 diff = abs(u.sun_sign.value - user.sun_sign.value)
                 if diff > 6:
                     user.compatibility_REST = (12 - diff) * .25
                 else:
                     user.compatibility_REST = diff * .25
            if u.moon_sign.value == user.moon_sign.value:
                 user.compatibility_REST += 1.2
            else:
                 diff = abs(u.moon_sign.value - user.moon_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .2
                 else:
                     user.compatibility_REST += diff * .2
            if u.rising_sign.value == user.rising_sign.value:
                 user.compatibility_REST += .9
            else:
                 diff = abs(u.rising_sign.value - user.rising_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .15
                 else:
                     user.compatibility_REST += diff * .15
            if u.mercury_sign.value == user.mercury_sign.value:
                 user.compatibility_REST += .6
            else:
                 diff = abs(u.mercury_sign.value - user.mercury_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .1
                 else:
                     user.compatibility_REST += diff * .1
            if u.venus_sign.value == user.venus_sign.value:
                 user.compatibility_REST += .6
            else:
                 diff = abs(u.venus_sign.value - user.venus_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .1
                 else:
                     user.compatibility_REST += diff * .1
            if u.mars_sign.value == user.mars_sign.value:
                 user.compatibility_REST += .6
            else:
                 diff = abs(u.mars_sign.value - user.mars_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .1
                 else:
                     user.compatibility_REST += diff * .1
            if u.jupiter_sign.value == user.jupiter_sign.value:
                 user.compatibility_REST += .6
            else:
                 diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
                 if diff > 6:
                     user.compatibility_REST += (12 - diff) * .1
                 else:
                     user.compatibility_REST += diff * .1
            user.compatibility_REST = round((user.compatibility_REST - 1) / 5.0 * 100.0, 1)
        queryset = sorted(queryset, key=operator.attrgetter('compatibility_REST'), reverse=True)
    serializer = IndividualSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)

class ZodiacViewSet(viewsets.ModelViewSet):
    queryset = Zodiac.objects.all()
    serializer_class= ZodiacSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class= LocationSerializer
    permission_classes = [permissions.IsAuthenticated]





def search(request):
    search = request.GET['search']
    search = search.split(" ")
    users = Individual.objects.filter(Q(first_name__in=search)|Q(last_name__in=search)|Q(user__username__in=search))
    if request.GET.get('page'):    
        page = int(request.GET['page'])
    else:
        page = 1
    if request.user.is_authenticated:
        u = Individual.objects.get(user=request.user) 
        for user in users:
            user.compatibility = 0.0
            if u.sun_sign.value == user.sun_sign.value:
                 user.compatibility = 1.5
            else:
                 diff = abs(u.sun_sign.value - user.sun_sign.value)
                 if diff > 6:
                     user.compatibility = (12 - diff) * .25
                 else:
                     user.compatibility = diff * .25
            if u.moon_sign.value == user.moon_sign.value:
                 user.compatibility += 1.2
            else:
                 diff = abs(u.moon_sign.value - user.moon_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .2
                 else:
                     user.compatibility += diff * .2
            if u.rising_sign.value == user.rising_sign.value:
                 user.compatibility += .9
            else:
                 diff = abs(u.rising_sign.value - user.rising_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .15
                 else:
                     user.compatibility += diff * .15
            if u.mercury_sign.value == user.mercury_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.mercury_sign.value - user.mercury_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.venus_sign.value == user.venus_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.venus_sign.value - user.venus_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.mars_sign.value == user.mars_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.mars_sign.value - user.mars_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.jupiter_sign.value == user.jupiter_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            user.compatibility = round((user.compatibility - 1) / 5.0 * 100.0, 1)
        pages = range(2, ceil(users.count() / 5) + 1)
        users = sorted(users, key=operator.attrgetter('compatibility'), reverse=True)[(page-1)*5:(page-1)*5+5]
    else:
        users = Individual.objects.all()
        pages = range(2, ceil(users.count() / 5) + 1)
        users = users[(page-1)*5:(page-1)*5+5]

    return render(request, 'index.html', {'users': users, 'pages': pages})


def unfriend(request):
    id = request.GET['id']
    ind = Individual.objects.get(pk=id)
    u = Individual.objects.get(user=request.user)
    f = Friendship.objects.filter(Q(ind1=ind)&Q(ind2=u)|Q(ind1=u)&Q(ind2=ind)).first()
    f.delete()
    return redirect(reverse('profile', kwargs={'id': id}))

def post_on_wall(request):
    to_id = request.POST["to_ind"]
    text = request.POST["text"]
    to_ind = Individual.objects.get(pk=to_id)
    from_ind = Individual.objects.get(user=request.user)
    p = Post(text=text, to_ind=to_ind, from_ind=from_ind)
    p.save()
    return redirect(reverse('profile', kwargs={'id': to_id}))

@csrf_exempt
def post_on_wall_REST(request):
    to_id = request.POST["to_ind"]
    text = request.POST["text"]
    from_id = request.POST["from_ind"]
    to_ind = Individual.objects.get(pk=to_id)
    from_ind = Individual.objects.get(pk=from_id)
    p = Post(text=text, to_ind=to_ind, from_ind=from_ind)
    p.save()
    serializer = PostSerializer(p, many=False)
    return JsonResponse(serializer.data, safe=True)

@csrf_exempt
def friend_request_REST(request):
    frm = request.POST["from"]
    to = request.POST["to"]
    ind1=Individual.objects.get(pk=frm)
    ind2=Individual.objects.get(pk=to)
    f = Friendship(ind1=ind1, ind2=ind2)
    f.save()
    return JsonResponse({}, safe=True)

def friend_request(request):
    frm = request.GET["from"]
    to = request.GET["to"]
    ind1=Individual.objects.get(pk=frm)
    ind2=Individual.objects.get(pk=to)
    f = Friendship(ind1=ind1, ind2=ind2)
    f.save()
    return HttpResponse("Success")

def set_last_seen(request):
    lat = request.GET["lat"]
    lng = request.GET["lng"]
    ll_str = str(lat) + ", " + str(lng)
    geolocator = Nominatim(user_agent="astro")
    location = geolocator.reverse(ll_str)
    suburb = location.raw["address"]["suburb"]
    city = location.raw["address"]["city"]
    state = location.raw["address"]["state"]
    country = location.raw["address"]["country"]
    place = suburb + ", " + city + ", " + state + ", " + country
    i = Individual.objects.get(user=request.user)
    loc = Location(name=place, latitude=lat, longitude=lng)
    loc.save()
    i.last_seen = loc
    i.save()
    return HttpResponse("Last seen in " + place + ".")

def upload_profile_pic(request):
    id = request.POST["id"]
    user = Individual.objects.get(pk=id)
    user.profile_pic = request.FILES["img"] 
    user.save()
    return redirect(reverse('profile', kwargs={'id': id}))

def profile(request, id):
    user = Individual.objects.get(pk=id)
    friends = Friendship.objects.filter((Q(ind1=user)|Q(ind2=user)), pending__in=[False])   
    friend_requests = None
    friendship = None
    posts = Post.objects.filter(to_ind=user).order_by("-date_time")
    if request.user.is_authenticated:
        u = Individual.objects.get(user=request.user)
        friendship = Friendship.objects.filter((Q(ind1=user)&Q(ind2=u))|Q(ind1=u)&Q(ind2=user)).first()
        user.compatibility = 0.0
        if u.sun_sign.value == user.sun_sign.value:
            user.compatibility = 1.5
        else:
            diff = abs(u.sun_sign.value - user.sun_sign.value)
            if diff > 6:
                user.compatibility = (12 - diff) * .25
            else:
                user.compatibility = diff * .25
        if u.moon_sign.value == user.moon_sign.value:
            user.compatibility += 1.2
        else:
            diff = abs(u.moon_sign.value - user.moon_sign.value)
            if diff > 6:
                user.compatibility += (12 - diff) * .2
            else:
                user.compatibility += diff * .2
        if u.rising_sign.value == user.rising_sign.value:
            user.compatibility += .9
        else:
            diff = abs(u.rising_sign.value - user.rising_sign.value)
            if diff > 6:
                user.compatibility += (12 - diff) * .15
            else:
                user.compatibility += diff * .15
        if u.mercury_sign.value == user.mercury_sign.value:
            user.compatibility += .6
        else:
            diff = abs(u.mercury_sign.value - user.mercury_sign.value)
            if diff > 6:
                user.compatibility += (12 - diff) * .1
            else:
                user.compatibility += diff * .1
        if u.venus_sign.value == user.venus_sign.value:
            user.compatibility += .6
        else:
            diff = abs(u.venus_sign.value - user.venus_sign.value)
            if diff > 6:
                user.compatibility += (12 - diff) * .1
            else:
                user.compatibility += diff * .1
        if u.mars_sign.value == user.mars_sign.value:
            user.compatibility += .6
        else:
            diff = abs(u.mars_sign.value - user.mars_sign.value)
            if diff > 6:
                user.compatibility += (12 - diff) * .1
            else:
                user.compatibility += diff * .1
        if u.jupiter_sign.value == user.jupiter_sign.value:
             user.compatibility += .6
        else:
             diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
             if diff > 6:
                 user.compatibility += (12 - diff) * .1
             else:
                 user.compatibility += diff * .1
        user.compatibility = round((user.compatibility - 1) / 5.0 * 100.0, 1)
        friend_requests = Friendship.objects.filter(ind2=u, pending__in=[True])
    return render(request, 'profile.html', {'posts': posts, 'user': user, 'friendship': friendship, 'friend_requests': friend_requests, 'friends': friends})

def deny_friend_request(request):
    id = request.GET["id"]
    u = Individual.objects.get(user=request.user)
    other = Individual.objects.get(pk=id)
    f = Friendship.objects.filter((Q(ind1=u)&Q(ind2=other))|Q(ind1=other)&Q(ind2=u)).first()
    f.delete()
    return redirect(reverse('profile', kwargs={"id": u.id}))



def accept_friend_request(request):
    id = request.GET["id"]
    u = Individual.objects.get(user=request.user)
    other = Individual.objects.get(pk=id)
    f = Friendship.objects.filter((Q(ind1=u)&Q(ind2=other))|Q(ind1=other)&Q(ind2=u)).first()
    f.pending = False
    f.save()
    return redirect(reverse('profile', kwargs={"id": u.id}))

def index(request):
    if request.GET.get('page'):    
        page = int(request.GET['page'])
    else:
        page = 1
    if request.user.is_authenticated:
        u = Individual.objects.get(user=request.user) 
        friendships = Friendship.objects.filter(Q(ind1=u)|Q(ind2=u), pending__in=[False])
        users = Individual.objects.all().exclude(user=request.user)
        for friendship in friendships:
             users = users.exclude(pk=friendship.ind1.id)
             users = users.exclude(pk=friendship.ind2.id)
        for user in users:
            user.compatibility = 0.0
            if u.sun_sign.value == user.sun_sign.value:
                 user.compatibility = 1.5
            else:
                 diff = abs(u.sun_sign.value - user.sun_sign.value)
                 if diff > 6:
                     user.compatibility = (12 - diff) * .25
                 else:
                     user.compatibility = diff * .25
            if u.moon_sign.value == user.moon_sign.value:
                 user.compatibility += 1.2
            else:
                 diff = abs(u.moon_sign.value - user.moon_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .2
                 else:
                     user.compatibility += diff * .2
            if u.rising_sign.value == user.rising_sign.value:
                 user.compatibility += .9
            else:
                 diff = abs(u.rising_sign.value - user.rising_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .15
                 else:
                     user.compatibility += diff * .15
            if u.mercury_sign.value == user.mercury_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.mercury_sign.value - user.mercury_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.venus_sign.value == user.venus_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.venus_sign.value - user.venus_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.mars_sign.value == user.mars_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.mars_sign.value - user.mars_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            if u.jupiter_sign.value == user.jupiter_sign.value:
                 user.compatibility += .6
            else:
                 diff = abs(u.jupiter_sign.value - user.jupiter_sign.value)
                 if diff > 6:
                     user.compatibility += (12 - diff) * .1
                 else:
                     user.compatibility += diff * .1
            user.compatibility = round((user.compatibility - 1) / 5.0 * 100.0, 1)
        pages = range(2, ceil(users.count() / 5) + 1)
        users = sorted(users, key=operator.attrgetter('compatibility'), reverse=True)[(page-1)*5:(page-1)*5+5]
    else:
        users = Individual.objects.all()
        pages = range(2, ceil(users.count() / 5) + 1)
        users = users[(page-1)*5:(page-1)*5+5]

    return render(request, 'index.html', {'users': users, 'pages': pages})

def signup(request):
    return render(request, 'signup.html')


@csrf_exempt
def process_signup_REST(request):
    print(request)
    print(request.POST)
    username = request.POST.get("username")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    dob = request.POST.get("dob")
    pob = request.POST.get("pob")
    gender = request.POST.get("gender")
    lat = request.POST.get("lat")
    lng = request.POST.get("lng")
    password = request.POST.get("password")
    password_confirmation = request.POST.get("password_confirmation")
    if password != password_confirmation: 
        return JsonResponse({"error": "Passwords must match"})
    else:
        loc = Location(latitude=lat, longitude=lng, name=pob)
        loc.save()
        if " " in username:
            return JsonResponse({"error": "No spaces allowed in username"})
        from django.contrib.auth.models import User
        user = User.objects.filter(username=username).first()
        if user:
            return JsonResponse({"error": "Username already taken"})
        if len(password) < 8:
            return JsonResponse({"error": "Passwords must be 8 or more characters"})
        #otherwise
        user = User.objects.create_user(username=username, password=password)
        dob = datetime.fromisoformat(dob.replace('  0000', ''))
        i = Individual(gender=gender, first_name=first_name, last_name=last_name, dob=dob, place_of_birth=loc)
        tz = tzwhere.tzwhere()
        timezone_str = tz.tzNameAt(float(lat), float(lng))
        timezone = pytz.timezone(timezone_str)
        dt = datetime.now()
        date = Datetime(str(dob.year) + "/" + str(dob.month) + "/" + str(dob.day), str(dob.hour) + ":" + str(dob.minute), timezone.utcoffset(dt) / timedelta(hours=1))
        pos = GeoPos(float(lat), float(lng))
        chart = Chart(date, pos)

        sun = floor((chart.getObject(const.SUN).lon / 30 + 4) % 12)
        moon = floor((chart.getObject(const.MOON).lon / 30 + 4) % 12)
        rising = floor((chart.getAngle(const.ASC).lon / 30 + 4) % 12)
        mercury = floor((chart.getObject(const.MERCURY).lon / 30 + 4) % 12)
        venus = floor((chart.getObject(const.VENUS).lon / 30 + 4) % 12)
        mars = floor((chart.getObject(const.MARS).lon / 30 + 4) % 12)
        jupiter = floor((chart.getObject(const.JUPITER).lon / 30 + 4) % 12)
        if sun==0:
            sun=12
        if moon==0:
            moon=12
        if rising==0:
            rising=12
        if mercury==0:
            mercury=12
        if venus==0:
            venus=12
        if mars==0:
            mars=12
        if jupiter==0:
            jupiter=12
        i.sun_sign = Zodiac.objects.get(value=sun)
        i.moon_sign = Zodiac.objects.get(value=moon)
        i.rising_sign = Zodiac.objects.get(value=rising)
        i.mercury_sign = Zodiac.objects.get(value=mercury)
        i.venus_sign = Zodiac.objects.get(value=venus)
        i.mars_sign = Zodiac.objects.get(value=mars)
        i.jupiter_sign = Zodiac.objects.get(value=jupiter)
        i.save()
        if i:
            user.save()
            i.user = user
            i.save()   
        else:
            user.delete()

def process_signup(request):
    username = request.POST["username"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    dob = request.POST["dob"]
    pob = request.POST["pob"]
    gender = request.POST["gender"]
    lat = request.POST["lat"]
    lng = request.POST["lng"]
    password = request.POST["password"]
    password_confirmation = request.POST["password_confirmation"]
    if password != password_confirmation: 
        messages.error(request, "Passwords must match")
        return render(request, 'signup.html')
    else:
        loc = Location(latitude=lat, longitude=lng, name=pob)
        loc.save()
        if " " in username:
            messages.error(request, "No spaces allowed in username")
            return redirect(reverse('signup'))
        from django.contrib.auth.models import User
        user = User.objects.filter(username=username).first()
        if user:
            messages.error(request,'User already exists')
            return redirect(reverse('signup'))
        if len(password) < 8:
            messages.error(request, 'Passwords must be 8 or more characters')
            return redirect(reverse('signup'))
        #otherwise
        user = User.objects.create_user(username=username, password=password)
        i = Individual(gender=gender, first_name=first_name, last_name=last_name, dob=dob, place_of_birth=loc)
        dob= dob.split("T")
        date = dob[0].replace("-", "/")
        tz = tzwhere.tzwhere()
        timezone_str = tz.tzNameAt(float(lat), float(lng))
        timezone = pytz.timezone(timezone_str)
        dt = datetime.now()
        date = Datetime(date, dob[1], timezone.utcoffset(dt) / timedelta(hours=1))
        pos = GeoPos(float(lat), float(lng))
        chart = Chart(date, pos)

        sun = floor((chart.getObject(const.SUN).lon / 30 + 4) % 12)
        moon = floor((chart.getObject(const.MOON).lon / 30 + 4) % 12)
        rising = floor((chart.getAngle(const.ASC).lon / 30 + 4) % 12)
        mercury = floor((chart.getObject(const.MERCURY).lon / 30 + 4) % 12)
        venus = floor((chart.getObject(const.VENUS).lon / 30 + 4) % 12)
        mars = floor((chart.getObject(const.MARS).lon / 30 + 4) % 12)
        jupiter = floor((chart.getObject(const.JUPITER).lon / 30 + 4) % 12)
        if sun==0:
            sun=12
        if moon==0:
            moon=12
        if rising==0:
            rising=12
        if mercury==0:
            mercury=12
        if venus==0:
            venus=12
        if mars==0:
            mars=12
        if jupiter==0:
            jupiter=12
        i.sun_sign = Zodiac.objects.get(value=sun)
        i.moon_sign = Zodiac.objects.get(value=moon)
        i.rising_sign = Zodiac.objects.get(value=rising)
        i.mercury_sign = Zodiac.objects.get(value=mercury)
        i.venus_sign = Zodiac.objects.get(value=venus)
        i.mars_sign = Zodiac.objects.get(value=mars)
        i.jupiter_sign = Zodiac.objects.get(value=jupiter)
        i.save()
        if i:
            user.save()
            i.user = user
            i.save()   
            auth_login(request, user)
            return redirect(reverse('profile', kwargs={'id': i.id}))
        else:
            return redirect(reverse('signup'))    

def process_logout(request):
    logout(request)
    messages.success(request, "Successfully logged out of Echt Buch")
    
    # clear messages
    storage = messages.get_messages(request)
    storage.used = True

    return redirect(reverse('index')) 

def process_login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        messages.success(request, "Logged in, welcome to Echt Buch.")
        i = Individual.objects.get(user=user)
        return redirect(reverse('profile', kwargs={'id': i.id}))
    else:
        messages.error(request, "Failed to log in due to incorrect password or username")
        return redirect(reverse('index'))   

def login(request):
    return render(request, 'login.html')
