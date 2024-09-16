import socket
import json
import datetime
from elasticsearch import Elasticsearch

class LogCollector:
    def __init__(self, host='0.0.0.0', port=514, es_host='localhost', es_port=9200):
        self.host = host
        self.port = port
        self.es = Elasticsearch([{'host': es_host, 'port': es_port}])

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Log Collector running on {self.host}:{self.port}...")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        log_entry = self.parse_log(data.decode('utf-8'))
                        self.store_log(log_entry)

    def parse_log(self, log_data):
        log_entry = json.loads(log_data)
        log_entry['timestamp'] = datetime.datetime.now().isoformat()
        return log_entry

    def store_log(self, log_entry):
        self.es.index(index='logs', body=log_entry)
        print(f"Log stored in Elasticsearch: {log_entry}")

if __name__ == "__main__":
    collector = LogCollector()
    collector.start()
