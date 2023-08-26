import requests
import json
import pyttsx3


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()




try:
    city = input("Enter the name of the city\n")
    url = f"https://api.weatherapi.com/v1/current.json?key=eba1e35124624b76984164033230708&q={city}"
    r = requests.get(url)
    # print(r.text)
    wdic = json.loads(r.text)
    temp = wdic["current"]["temp_c"]
    date = wdic["location"]["localtime"]
    weather = f"Temperate at  {date} ,in {city}, is {temp} degrees Celsius"
    text_to_speech(weather)
except Exception as e:
    print("Some error occured ",e)



# {"location":{"name":"Indore","region":"Madhya Pradesh","country":"India","lat":22.72,"lon":75.83,"tz_id":"Asia/Kolkata","localtime_epoch":1691426965,"localtime":"2023-08-07 22:19"},"current":{"last_updated_epoch":1691426700,"last_updated":"2023-08-07 22:15","temp_c":24.0,"temp_f":75.2,"is_day":0,"condition":{"text":"Partly cloudy","icon":"//cdn.weatherapi.com/weather/64x64/night/116.png","code":1003},"wind_mph":13.6,"wind_kph":22.0,"wind_degree":260,"wind_dir":"W","pressure_mb":1007.0,"pressure_in":29.74,"precip_mm":0.0,"precip_in":0.0,"humidity":83,"cloud":75,"feelslike_c":26.4,"feelslike_f":79.4,"vis_km":6.0,"vis_miles":3.0,"uv":1.0,"gust_mph":15.7,"gust_kph":25.2}}
