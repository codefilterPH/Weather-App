
from django.shortcuts import render, redirect
from django.http import HttpResponse
# folium is for embedding the map
import folium
import geocoder
from .models import *
from .forms import *
import requests

# Create your views here.
def index(request):
    # if user will search
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()

    if Search.objects.all().last():
        address = Search.objects.all().last()
    else:
        Search.objects.create(address="Philippines")

    if address != "":
        try:
            # convert address to lat and lng
            location = geocoder.osm(address)
            latitude = location.lat
            longitude = location.lng
            country = location.country
            # load countries and cities
            countries = Countries.objects.all()
            cities = City.objects.all()

            # Create info objects integrate open weather
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1a768344c598363a91cbd9829ab995b1'
            weather_data = []
            city_weather = requests.get(url.format(address)).json()
            weather = {
                'city': address,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
                'speed': city_weather['wind']['speed'],
                'degree': city_weather['wind']['deg'],
                'pressure': city_weather['main']['pressure'],
                'time': city_weather['timezone']
            }
            weather_data.append(weather)
            # generate map
            map = folium.Map(location=[latitude, longitude], tiles='openstreetmap', zoom_start=6, control_scale=True)
            folium.Marker([latitude, longitude], tooltip=country,
                          popup=f'<p id="latlon">{latitude}, {longitude}</p>', ).add_to(
                map)
            map.add_child(folium.LatLngPopup())
            # Get representation of map objects
            map = map._repr_html_()
            context = {
                'map': map, 'form': form, 'weather_data': weather_data, 'countries': countries, 'cities': cities,
            }
            return render(request, 'index.html', context)
        except:
            address.delete()
            return HttpResponse("Not Found! Please try city or country")
    else:
        return HttpResponse("Address is empty, Status not found.")




def click(request, pk):
    country = pk
    if pk != "" or pk is None:
        add_country = Search(address=country)
        add_country.save()
    return redirect('/')


def learn_bootstrap(request):
    return render(request, 'practice.html')
