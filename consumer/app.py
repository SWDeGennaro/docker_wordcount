from kafka import KafkaConsumer, KafkaClient
from redis import Redis
import os

redis = Redis(host="redis", port=6379)
#kafka = KafkaClient(os.environ['KAFKA_1_PORT_9092_TCP_ADDR'] + ':9092')
kafka = KafkaClient('kafka:9092')
consumer = SimpleConsumer(kafka, "word-group", "word-topic")
consumer.seek(0, 0) #to start reading from the beginning of the queue.
#consumer.seek(0, 1) #to start reading from current offset.
#consumer.seek(0, 2) #to skip all the pending messages and start reading only new 

for message in consumer:
	# message value is raw byte string -- decode if necessary!
 	# e.g., for unicode: `message.value.decode('utf-8')`
	redis.incr(message.value)