from flask import Flask, Response, jsonify
from redis import Redis

app = Flask(__name__)
redis = Redis(host="redis", port=6379)

#@app.route('/')
#def hello():
#	redis.incr('hits')
#	return 'Hello from Compose Test! I have been see %s . \n' % redis.get('hits')

@app.route('/words')
def words():
    words = {"de":8,"la":6,"atl\u00e9tico":6,"el":4,"madrid":4,"y":4,"vs":3,"masih":3,"champions":3,"0-0":3}

    response = Response(words)

    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
