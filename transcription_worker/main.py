import os
import whisper
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
import json
import tempfile
from dotenv import load_dotenv
from extractors.audio_extractor_factory import AudioExtractorFactory
from internal_api import update_status_in_db


model = whisper.load_model("base")


def callback(ch:BlockingChannel, method:Basic.Deliver, properties:BasicProperties, body:bytes):
    print(f"[*] Received message for transcription...")
    try:
        message = json.loads(body.decode('utf-8'))
        with tempfile.TemporaryDirectory() as tmpdir:
            extractor = AudioExtractorFactory.get_extractor(message["source_type"])
            update_status_in_db(video_id=message["id"],new_status="extracting_media")
            path = extractor.download_and_extract(message["url"], tmpdir)

            update_status_in_db(video_id=message["id"],new_status="transcribing")
            result = whisper.transcribe(model=model,audio=path)
            segments = []
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            output={
                "source_type":message["source_type"],
                "id":message["id"],
                "message":segments
            }
            print(output)
            ch.basic_publish(exchange='semantic_search_exchange',
                             routing_key='video.embedding',
                             body=(json.dumps(output)).encode("utf-8"),
                             properties=pika.BasicProperties(
                                 content_type='application/json',
                                 delivery_mode=pika.DeliveryMode.Persistent
                                )
                             )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[!] Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


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

    queue_name = 'transcription_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    routing_key = 'video.transcribe'
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

    next_queue_name="embedding_queue"
    channel.queue_declare(queue=next_queue_name,durable=True)
    next_routing_key="video.embedding"
    channel.queue_bind(queue=next_queue_name,
                       exchange=exchange_name,
                       routing_key=next_routing_key)

    print(f"[*] Waiting for messages in queue '{queue_name}'... To exit press CTRL+C")
    channel.start_consuming()


if __name__ == '__main__':
    main()