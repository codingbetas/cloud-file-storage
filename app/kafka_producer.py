from kafka import KafkaProducer
import json

# Connect to the Kafka broker running in Docker
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_upload_event(filename: str, file_size: int):
    """Sends a message to the 'file-uploads' Kafka topic."""
    event = {
        "event_type": "FILE_UPLOADED",
        "filename": filename,
        "size_bytes": file_size
    }
    try:
        producer.send('file-uploads', value=event)
        producer.flush()
        print(f"📡 Sent Kafka event for {filename}")
    except Exception as e:
        print(f"❌ Failed to send Kafka event: {e}")