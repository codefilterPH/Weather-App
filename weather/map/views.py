from django.shortcuts import render, redirect
from django.http import HttpResponse
#folium is for embedding the map
import folium
import geocoder
from .models import *
from .forms import *
import requests
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    location = geocoder.osm(address)
    latitude = location.lat
    longitude = location.lng
    country = location.country
    if latitude == None or longitude == None:
        address.delete()
        return HttpResponse("Your address input is invalid")
    else:
        #Create info objects integrate open weather
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1a768344c598363a91cbd9829ab995b1'
        weather_data = []
        city_weather =requests.get(url.format(address)).json()
        weather = {
            'city':address,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'speed': city_weather['wind']['speed'],
            'degree': city_weather['wind']['deg'],
            'time': city_weather['dt']
    
        }
        weather_data.append(weather)



    #Create map object
    map = folium.Map(location=[latitude,longitude], zoom_start=8, control_scale=True)
    folium.Marker([latitude, longitude], tooltip="Click for more info",popup=country).add_to(map)
    #Get representation of map objects
    map = map._repr_html_()

    context = {
        'map':map,'form':form, 'weather_data':weather_data
    }
    return render(request, 'index.html', context)
