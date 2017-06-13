from flask import Flask, abort, request
import requests
from datetime import datetime
from weather_API import API_KEY
from news_list import all_news

city_id = 524901

app = Flask(__name__)


def get_weather(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        print('Something went wrong')


@app.route('/')
def index():
    weather = get_weather('http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&lang=ru&APPID={}'.format(city_id,
                                                                                                           API_KEY))
    today = datetime.now().strftime('%d.%m.%Y')
    temp = '{}. Температура {} {}'.format(weather['name'], today, weather['main']['temp'])
    return temp


@app.route('/news')
def all_the_news():
    colors = ['green', 'blue', 'red', 'yellow', 'black', 'white']
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = 10
    color = request.args.get('color') if request.args.get('color') in colors else 'black'
    return '<h1 style="color: %s">News:  <small>%s</small></h1>' % (color, limit)


@app.route('/news/<int:news_id>')
def news_by_id(news_id):
    news_to_show = [news for news in all_news if news['id'] == news_id]
    if len(news_to_show) == 1:
        result = '<h1>%(title)s</h1><p><i>%(date)s</i></p><p>%(text)s</p>'
        result = result % news_to_show[0]
        return result
    else:
        abort(404)


if __name__ == '__main__':
    app.run()


