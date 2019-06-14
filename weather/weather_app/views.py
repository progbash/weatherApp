import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=e9e7b90c2e9315e6370b53013e324984&units=metric'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/index.html', context)


