import requests

API_KEY = "62acfe029ef72824cce2ced7d280874e"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url).json()

        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        rain = response.get("rain", {}).get("1h", 0)

        return temp, humidity, rain

    except:
        return None, None, None