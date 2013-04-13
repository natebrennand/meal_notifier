from flask import Flask, render_template, g
from secrets import columbia_token
import sqlite3 as lite
import requests
import json

app = Flask(__name__)


@app.before_request
def before_request():
    g.db = connect_db()


def connect_db():
    return lite.connect('data.db')


@app.route('/')
def home():
    get_food()
    return render_template('index.html')


@app.route('/choose')
def choose():
    return render_template('choose.html', meals=get_meal_items('DN'))


@app.route('/sign-up', methods=['POST'])
def signed_up():
    return render_template('sign-up.html')


def get_meal_items(meal_name):
    cursor = g.db.cursor()
    sql_query = """
    SELECT DISTINCT
        F.food_name
    FROM
        food F
    WHERE
        F.meal_type = "{}"
    ORDER BY
        F.food_name;
    """.format(meal_name)
    cursor.execute(sql_query)
    temp = cursor.fetchall()
    return temp


def get_food(table_name="food"):
    cursor = g.db.cursor()
    sql_init = '''
    CREATE TABLE if NOT EXISTS {} (
        food_name TEXT,
        meal_type TEXT,
        PRIMARY KEY (food_name ASC)
    );
    '''.format(table_name)
    cursor.execute(sql_init)

    payload = {'api_token': columbia_token, 'meal_after': '2013-03-02',
               'pretty': 'true'}
    r = requests.get('http://data.adicu.com/dining', params=payload)
    r_json = json.loads(r.text)

    for meal in r_json['data']:
        meal_type = meal['meal_type']
        for item in meal['menu']:
            sql_insert = """
            INSERT or IGNORE
            INTO food VALUES ("{}","{}");""".format(item, meal_type)
            cursor.execute(sql_insert)
            g.db.commit()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

if __name__ == "__main__":
    app.debug = True
    app.run()
