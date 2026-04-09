import os
import json
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from dotenv import load_dotenv

from chunker import chunker
from embeddings.embedding_provider_factory import get_embedding_provider
from internal_api import update_status_in_db
from database.repository import VectorDBRepository


class EmbeddingWorker:
    def __init__(self):
        print("[*] Initializing Worker Dependencies...")
        self.provider = get_embedding_provider()
        self.db = VectorDBRepository(
            collection_name=self.provider.collection_name,
            dimension=self.provider.dimension
        )

        self.queue_name = 'embedding_queue'
        self.exchange_name = 'semantic_search_exchange'
        self.routing_key = 'video.embedding'

    def setup_rabbitmq(self) -> BlockingChannel:

        rabbitmq_url = os.environ.get("RABBITMQ_URL")
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct', durable=True)
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.routing_key)

        channel.basic_qos(prefetch_count=1)

        return channel

    def process_message(self, ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):

        try:
            message = json.loads(body.decode("utf-8"))
            content_id = message["id"]

            print(f"\n[->] Processing video: {content_id}")

            chunks = chunker(
                segments=message["message"],
                min_words=15, max_words=60, max_time_sec=40, overlap_segments=2
            )

            update_status_in_db(video_id=content_id, new_status="generating_vectors")
            vectorized_chunks = self.provider.generate_embeddings(chunks)

            self.db.save_embedded_chunks(video_id=content_id, chunks=vectorized_chunks)

            update_status_in_db(video_id=content_id, new_status="ready")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"[V] Successfully finished video {content_id}")

        except Exception as e:
            print(f"[X] Error processing message: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        channel = self.setup_rabbitmq()
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message,
            auto_ack=False
        )
        print(f"[*] Waiting for messages in queue '{self.queue_name}'... To exit press CTRL+C")
        channel.start_consuming()


def main():
    load_dotenv()
    worker = EmbeddingWorker()
    worker.start()


if __name__ == '__main__':
    main()