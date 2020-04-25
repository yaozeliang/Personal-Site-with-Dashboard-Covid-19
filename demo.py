import requests

url = 'http://api.openweathermap.org/data/2.5/weather?q=Paris,fr&units=imperial&appid=2e37fd2364d867821f298280137eecc0'
r = requests.get(url).json()
paris_weather={}

if r['cod']==200:
    paris_weather = {
    'city':'Paris',
    'temperature' :float("{0:.2f}".format((r['main']['temp']-32)* 5/9)),
    'description' : r['weather'][0]['description'],
    'icon' : r['weather'][0]['icon'],
    'country':r['sys']['country']}


