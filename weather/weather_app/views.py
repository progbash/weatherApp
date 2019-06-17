import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=e9e7b90c2e9315e6370b53013e324984&units=metric'

    error_message = ''
    message = ''
    message_css = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    error_message = "Such city doesn't exist in the world :("
            else:
                error_message = 'City has already been selected.'

    if error_message:
        message = error_message
        message_css = 'warning'
    else:
        message = 'City added successfully !'
        message_css = 'success'

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

    context = {
        'weather_data': weather_data,
        'form': form,
        'message': message,
        'message_css': message_css
    }
    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

