from django.shortcuts import render, redirect
from django.http import HttpResponse
#folium is for embedding the map
import folium
import geocoder
from .models import *
from .forms import *
import requests
import jinja2
from jinja2 import Template
from folium.map import Marker
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

    #removed invalid input
    if latitude == None or longitude == None:
        address.delete()
        return HttpResponse("Your address input is invalid")
    elif latitude == None and longitude == None:
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
            'pressure': city_weather['main']['pressure'],
            'time': city_weather['timezone']
        }
        weather_data.append(weather)

    tmpldata = """<!-- monkey patched Marker template -->
    {% macro script(this, kwargs) %}
        var {{ this.get_name() }} = L.marker(
            {{ this.location|tojson }},
            {{ this.options|tojson }}
        ).addTo({{ this._parent.get_name() }}).on('click', onClick);
    {% endmacro %}
    """

    Marker._mytemplate = Template(tmpldata)

    def myMarkerInit(self, *args, **kwargs):
        self.__init_orig__(*args, **kwargs)
        self._template = self._mytemplate

    Marker.__init_orig__ = Marker.__init__
    Marker.__init__ = myMarkerInit

    #Create map object
    map = folium.Map(location=[latitude,longitude], zoom_start=14, control_scale=True)
    folium.Marker([latitude, longitude], tooltip=country, popup=f'<p id="latlon">{latitude}, {longitude}</p>').add_to(map)
    map.add_child(folium.LatLngPopup())

    el = folium.MacroElement().add_to(map)
    el._template = jinja2.Template("""
        {% macro script(this, kwargs) %}
        function copy(text) {
            var input = document.createElement('textarea');
            input.innerHTML = text;
            document.body.appendChild(input);
            input.select();
            var result = document.execCommand('copy');
            document.body.removeChild(input);
            return result;
        };

        function getInnerText( sel ) {
            var txt = '';
            $( sel ).contents().each(function() {
                var children = $(this).children();
                txt += ' ' + this.nodeType === 3 ? this.nodeValue : children.length ? getInnerText( this ) : $(this).text();
            });
            return txt;
        };

        function onClick(e) {
           var popup = e.target.getPopup();
           var content = popup.getContent();
           text = getInnerText(content);
           copy(text);
        };
        {% endmacro %}
    """)

    # Get representation of map objects
    map = map._repr_html_()

    context = {
        'map':map,'form':form, 'weather_data':weather_data
    }
    return render(request, 'index.html', context)
