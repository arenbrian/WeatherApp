from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'c5e4fa23075ee68c26a4a1b3c3ce6bd8'

@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')

        if city:
            weather = get_weather(city)
            if weather is None:
                error = "Could not retrieve weather data. Please try again."

    return render_template('index.html', weather=weather, error=error)

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial'
    response = requests.get(url)
    
    
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    try:
        response_data = response.json()
        print(f"Response JSON: {response_data}")  
    except ValueError:
        print("Error: Unable to parse JSON response.")
        return None

    if response.status_code == 200:
        if 'main' in response_data and 'temp' in response_data['main']:
            weather = {
                'city': response_data.get('name', 'Unknown location'),
                'temperature': response_data['main']['temp'],
                'description': response_data['weather'][0]['description'],
                'icon': response_data['weather'][0]['icon'],
            }
            return weather
        else:
            print("Error: 'main' or 'temp' key not found in the API response.")
            return None
    else:
        print(f"Error: API request failed with status code {response.status_code}")
        if 'message' in response_data:
            print(f"API Error Message: {response_data['message']}")
        return None




if __name__ == '__main__':
    app.run(debug=True)
