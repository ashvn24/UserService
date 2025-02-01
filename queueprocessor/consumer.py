import pika

class MPQConsumer:
    def __init__(self, queue_name: str, max_priority: int = 10, 
                 rabbitmq_url: str = "amqps://emfkgxyq:qxdAqhKCwAJtyQyZU8WzwAUOCfgrpXmg@possum.lmq.cloudamqp.com/emfkgxyq"):
        self.queue_name = queue_name
        self.max_priority = max_priority
        self.connection_params = pika.URLParameters(rabbitmq_url)
        self._ensure_queue()
        
    def _ensure_queue(self):
        """Ensure queue exists with correct settings"""
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(
            queue=self.queue_name,
            arguments={"x-max-priority": self.max_priority}
        )
        connection.close()

    def consume(self, callback):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        
        def on_message(ch, method, properties, body):
            print(f"Received message: {body}")
            # callback(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=self.queue_name, on_message_callback=on_message)
        print(f"Waiting for messages on queue {self.queue_name}...")
        channel.start_consuming()