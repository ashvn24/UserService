import pika
from typing import Optional

class QueueManager:
    def __init__(self, queue_name: str, max_priority: int = 10, 
                 rabbitmq_url: str = "amqps://emfkgxyq:qxdAqhKCwAJtyQyZU8WzwAUOCfgrpXmg@possum.lmq.cloudamqp.com/emfkgxyq"):
        self.queue_name = queue_name
        self.max_priority = max_priority
        self.connection_params = pika.URLParameters(rabbitmq_url)
        
    def setup_queue(self) -> None:
        """Set up queue with proper configuration, deleting if it exists"""
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        
        try:
            # First try to delete the queue if it exists
            channel.queue_delete(queue=self.queue_name)
        except Exception as e:
            print(f"Queue deletion error (can be ignored if queue doesn't exist): {e}")
            
        try:
            # Now declare the queue with proper settings
            channel.queue_declare(
                queue=self.queue_name,
                arguments={"x-max-priority": self.max_priority}
            )
            print(f"Queue {self.queue_name} successfully configured with max priority {self.max_priority}")
        finally:
            connection.close()