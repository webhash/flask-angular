from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import redis
import json 
import datetime
import logging
import os


# we create a key by the name of index that stores the latest value 
index_key_name = 'index'
# we pass redis so that we can use the --link feature of the dockers 
database = redis.StrictRedis(host='redis', port=6379, db=0)
# we intialize the index to zero
database.set(index_key_name, 0)

# create the flask app
app = Flask(__name__)
CORS(app)

# enable looging to file so that when user runs the docker 
# container in non-interactive mode they can check the logs via file
@app.before_first_request
def set_logger():
	log_level = logging.INFO
	root = os.path.dirname(os.path.abspath(__file__))
	logdir = os.path.join(root, 'logs')
	if not os.path.exists(logdir):
		os.mkdir(logdir)
	log_file = os.path.join(logdir, 'app.log')
	handler = logging.FileHandler(log_file)
	handler.setLevel(log_level)
	app.logger.addHandler(handler)
	app.logger.setLevel(log_level)

def invalid_json_request():
	app.logger.info("Either user didnt send json or json doesnt contain the 'input' key")
	data = {
		"Name": "Invalid JSON request",
		"Description": "Please post a json request with input as the key"
	}
	response = app.response_class(
		response=json.dumps(data),
		status=400,
		mimetype='application/json'
	)
	return response

def get_handler():
	app.logger.info("Inside get_handler")
	assert request.method == 'GET'
	return '\nYes I Can Hear You !!! \nbut I only talk with POST\n\n'

def post_handler():
	app.logger.info("Inside post_handler")
	assert request.method == 'POST'
	if(request.is_json):
		app.logger.info("Request is json type")
		req_data = request.get_json()
		if 'input' in req_data:
			app.logger.info("Request contains 'input' key")
			# we only care about the first 20 characters 
			key = req_data['input'][:20]
			
			index_key = None
			
			if key in database:
				app.logger.info("input key already exists in database")
				# here we need to convert to int
				index_key = int(database.get(key).decode('utf-8'))
				app.logger.debug('index type is ' + str(type(index_key)))
				app.logger.debug('index value is ' + str(index_key))
			else:
				app.logger.info("input key doesn't exists in database")
				# increment operater returns int :D
				index_key = database.incr(index_key_name)
				app.logger.debug('index type is ' + str(type(index_key)))
				app.logger.debug('index value is ' + str(index_key))
				database.set(key, index_key)

			if index_key != None:
				mod_key = "success['" + key + "']"
			else:
				mod_key = "fail['" + key + "']"
				app.logger.error("somehow we failed to manage the key")
				
			app.logger.info('modified key value is ' + mod_key)
			
			return jsonify(
				response=mod_key,
				index=index_key
			)
			
		else:
			return invalid_json_request()
	else:
		return invalid_json_request()
		
	
@app.route('/', methods=['GET','POST'])
def request_handler():
	if request.method == 'GET':
		return get_handler()
	elif request.method == 'POST':
		return post_handler()


# change port according to the requirement 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)