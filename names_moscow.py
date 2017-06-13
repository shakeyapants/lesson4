import requests
from flask import Flask, request
from moscow_API import API_KEY
from datetime import date

names_from = 'https://apidata.mos.ru/v1/datasets/2009/rows?api_key={}'.format(API_KEY)
current_year = date.today().year

app = Flask(__name__)


def get_names(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        print('Something went wrong')


@app.route('/')
def hi():
    return 'Hi'


@app.route('/names')
def names_table():
    accepted_years = range(2015, current_year + 1)
    try:
        year = int(request.args.get('year')) if int(request.args.get('year')) in accepted_years else 2017
    except:
        year = 2017
    names_data = get_names(names_from)
    header = '<table>' \
           '    <tr>' \
           '        <th>Год</th>' \
           '        <th>Месяц</th>' \
           '        <th>Имя</th>' \
           '        <th>Количество</th>' \
           '    </tr>'
    row = ''
    for i in range(len(names_data)):
        if int(names_data[i]['Cells']['Year']) == year:
            row += '<tr>' \
                   '    <td>%(Year)s</td>' \
                   '    <td>%(Month)s</td>' \
                   '    <td>%(Name)s</td>' \
                   '    <td>%(NumberOfPersons)s</td>' \
                   '</tr>' % names_data[i]['Cells']

    end = '</table>'
    return header + row + end


if __name__ == '__main__':
    app.run()