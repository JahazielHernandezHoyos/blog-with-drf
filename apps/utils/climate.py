from bs4 import BeautifulSoup
import requests

def get_climate():
    try:
        url = 'https://weather.com/es-AR/tiempo/hoy/l/ARBA0009:1:AR'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        location = soup.find('h1', class_='CurrentConditions--location--1YWj_').get_text()
        weather = soup.find('div', class_='CurrentConditions--phraseValue--mZC_p').get_text()
        temperature_today = soup.find('span', class_='CurrentConditions--tempValue--MHmYY').get_text()
        daily_weather = []
        daily_weather_container = soup.find_all('li', class_='Column--column--3tAuz')
        for i, container in enumerate(daily_weather_container):
            if i >= 9:
                day = container.find('span', class_='Ellipsis--ellipsis--3ADai').get_text().capitalize()
                temperature = container.find('div', class_='Column--temp--1sO_J').get_text()
                if temperature == '--':
                    temperature = temperature_today
                weather = container.find('svg', class_='Column--weatherIcon--2w_Rf Icon--icon--2aW0V Icon--fullTheme--3Fc-5').get_text()
                daily_weather.append({'day': day, 'temperature': temperature, 'weather': weather})
        data = {
            'location': location,
            'today': {
                'weather': weather,
                'temperature': temperature_today,
            },
            'week': daily_weather
        }
        return data
    except Exception as e:
        raise Exception('Error on getting weather data')