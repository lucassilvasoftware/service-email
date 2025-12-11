from kafka import KafkaProducer
from os import path, getcwd
from dotenv import dotenv_values
from datetime import datetime
from json import dumps


config_path = path.join(getcwd(), 'env', 'credentials.cfg')
config = dotenv_values(config_path)
IP_ADDRESS = config['SERVER_IP']


class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=IP_ADDRESS,
                                      value_serializer=lambda v: dumps(v).encode('utf-8'))

    def send_message(self, topic, message):
        """Enviar registro de log ou relacionado em algum tópico"""
        self.producer.send(topic, value=message)
        self.producer.flush()
        # self.producer.close()

    def send_message_job(self, topic, base64_func, args):
        """Enviar job para ser processado em algum tópico"""
        job = {
            'func': base64_func,
            'args': args,
            'timestamp': str(datetime.now())
        }
        self.producer.send(topic, value=job)
        self.producer.flush()
        self.producer.close()
