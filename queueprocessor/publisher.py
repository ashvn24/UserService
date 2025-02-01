import pika

class MPQPublisher:
    def __init__(self, queue_name: str, max_priority: int = 10, 
                 rabbitmq_url: str = "amqps://emfkgxyq:qxdAqhKCwAJtyQyZU8WzwAUOCfgrpXmg@possum.lmq.cloudamqp.com/emfkgxyq"):
        self.queue_name = queue_name
        self.max_priority = max_priority
        self.connection_params = pika.URLParameters(rabbitmq_url)
        self.channel = None
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

    def connect(self):
        connection = pika.BlockingConnection(self.connection_params)
        self.channel = connection.channel()

    def publish(self, message: str, priority: int = 0):
        if self.channel is None:
            self.connect()
            
        # Ensure priority is within bounds
        priority = max(0, min(priority, self.max_priority))
            
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(priority=priority)
        )
        print(f"Published message: {message} with priority: {priority}")