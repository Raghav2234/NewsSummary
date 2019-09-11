from flask import Flask, jsonify, request
from flask_cors import CORS
from NewsSummarizer import populate
import multiprocessing
import os

app = Flask(__name__)
CORS(app)
populate.update_news()
data, dbconnected = populate.retrieve_data()
@app.route('/news')
@app.route('/')
def get_news():
	global data, dbconnected
	if not dbconnected:
		data, dbconnected = populate.retrieve_data()
	return jsonify(result=data)

p2 = multiprocessing.Process(target=populate.schedule)
p2.start()
	
if __name__ == '__main__':
	print("app started")
	app.run()	
p2.join()


