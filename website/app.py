from flask import Flask, render_template, Response, jsonify
from redis import Redis

app = Flask(__name__)
redis = Redis(host="redis", port=6379)

words = {
	'one': 5,
	'two': 1,
	'three': 3,
	'seven': 9,
	'ten':3,
	'eleven': 2
}

for key in words.keys():
   redis.set(key, words[key])

#@app.route('/')
#def hello():
#	redis.incr('hits')
#	return 'Hello from Compose Test! I have been see %s . \n' % redis.get('hits')

@app.route('/')
def index():
    # Render template
    return render_template('index.html')

@app.route('/words')
def words():
	result = {}
	for k in redis.keys():
		result[k] = redis.get(k)

	response = Response(jsonify(**result))

	response.headers.add('Access-Control-Allow-Origin', "*")

	return response

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
