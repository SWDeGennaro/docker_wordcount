from flask import Flask, render_template, request, jsonify
from kafka import SimpleProducer, KafkaClient
import os

app = Flask(__name__)
kafka = KafkaClient(os.environ['KAFKA_1_PORT_9092_TCP_ADDR'] + ':9092')
producer = SimpleProducer(kafka)
topic = "word-topic"

@app.route('/')
def index():
    # Render template
    return render_template('index.html')

@app.route('/post', methods = ['POST'])
def post():
    # Get the parsed contents of the form data
    json = request.json
    print(json)
    producer.send_messages(topic, jsonify(json))

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
