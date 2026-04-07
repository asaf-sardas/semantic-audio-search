import os
import whisper
import pika
import json
import tempfile
from dotenv import load_dotenv
from extractors.audio_extractor_factory import AudioExtractorFactory


model = whisper.load_model("base")


def callback(ch, method, properties, body):
    print(f"[*] Received message for transcription...")
    try:
        message = json.loads(body.decode('utf-8'))
        with tempfile.TemporaryDirectory() as tmpdir:
            extractor = AudioExtractorFactory.get_extractor(message["source_type"])
            # TODO change status to extracting media in DB
            path = extractor.download_and_extract(message["url"], tmpdir)
            # TODO change status to transcribing in DB
            result = whisper.transcribe(model=model,audio=path)
            segments_data = []
            for segment in result["segments"]:
                print(segment)
                segments_data.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })
            # TODO publish to embedding_q


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

    print(f"[*] Waiting for messages in queue '{queue_name}'... To exit press CTRL+C")
    channel.start_consuming()


if __name__ == '__main__':
    main()