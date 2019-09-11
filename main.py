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

print(int(os.environ['PORT']))
# def server_start():
# 	#app.run(debug=True)
# 	app.run(port = int(os.environ['PORT']))

# if __name__ == '__main__':
# def main(a, b):
# p2 = multiprocessing.Process(target=populate.schedule)
# p2.start()
# p2.join()
