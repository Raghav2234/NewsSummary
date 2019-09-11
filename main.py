from flask import Flask, jsonify, request
from flask_cors import CORS
from NewsSummarizer import populate
import multiprocessing


app = Flask(__name__)
CORS(app)

@app.route('/news')
@app.route('/')
def get_news():
	global data, dbconnected
	if not dbconnected:
		data, dbconnected = populate.retrieve_data()
	return jsonify(result=data)


def server_start():
	#app.run(debug=True)
	app.run(host=env.HOST, debug=env.DEBUG, port=env.PORT)

if __name__ == '__main__':
	populate.update_news()
	data, dbconnected = populate.retrieve_data()
	p1 = multiprocessing.Process(target=server_start)
	p2 = multiprocessing.Process(target=populate.schedule)
	p2.start()
	p1.start()
	p2.join()
	p1.join()
