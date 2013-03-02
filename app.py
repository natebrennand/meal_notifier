from flask import Flask, render_template
import sqlite3 as lite
import requests

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

def start_db(cursor, table_name="data"):
	sql_init = '''
	CREATE TABLE if NOT EXISTS {} (
		phone_num INTEGER,
		name TEXT,
		random_id INTEGER
	)
	'''.format(table_name)
	cursor.execute(sql_init)





if __name__ == "__main__":
	app.debug = True
	app.run()


