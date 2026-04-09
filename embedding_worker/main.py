import os
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import json
import requests
from dotenv import load_dotenv
from chunker import chunker
from embeddings.embedding_provider_factory import get_embedding_provider

embedding_provider = get_embedding_provider()

def callback(ch:BlockingChannel, method:Basic.Deliver, properties:BasicProperties, body:bytes):
    message=json.loads(body.decode("utf-8"))
    chunks=chunker(segments=message["message"],min_words=15,max_words=60,max_time_sec=40,overlap_segments=2)
    vectorized_chunks=embedding_provider.generate_embeddings(chunks)



def main():
    load_dotenv()
    rabbitmq_url = os.environ.get("RABBITMQ_URL")
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()

    exchange_name = 'semantic_search_exchange'
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct',
        durable=True
    )

    queue_name = 'embedding_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    routing_key = 'video.embedding'
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=routing_key
    )

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )

    print(f"[*] Waiting for messages in queue '{queue_name}'... To exit press CTRL+C")
    channel.start_consuming()


if __name__ == '__main__':
    main()