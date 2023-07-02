import socket
import json

BUFF_SIZE = 2 ** 13


class Tracker:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.ip, self.port)
        self.file_tracker = {}

    def run(self):
        self.sock.bind(self.server_address)
        print(f"O tracker está aguardando requisições em {self.ip}:{self.port}")
        while True:
            data, address = self.sock.recvfrom(BUFF_SIZE)
            data = data.decode('utf-8')
            print(f"Requisição recebida de {address}:\n{data}")
            data = json.loads(data)
            response = self.handle_request(data)
            if response:
                response = json.dumps(response).encode('utf-8')
                self.sock.sendto(response, address)
                print(f"Resposta enviada para o nó {address}: {response}")

    def handle_request(self, data):
        request_type = data.get('type')
        if request_type == 'add_peer':
            return self.handle_add_peer(data)
        elif request_type == 'find_file':
            return self.handle_find_file(data)

    def handle_add_peer(self, data):
        file_name = data['file_name']
        chunks = data.get('chunks', [-1])
        score = 100 if 'chunks' in data else 0

        if file_name not in self.file_tracker:
            self.file_tracker[file_name] = {
                'peers': [],
                'chunk_count': data['chunk_count']
            }

        self.file_tracker[file_name]['peers'].append({
            'peer_addr': data['peer_addr'],
            'score': score,
            'chunk_list': chunks
        })

    def handle_find_file(self, data):
        file_name = data['file_name']
        return self.file_tracker.get(file_name, {})


if __name__ == '__main__':
    tracker = Tracker('localhost', 1111)
    tracker.run()
