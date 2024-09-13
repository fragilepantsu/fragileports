import sys
import socket
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import random
import string
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def handle_client(connection, client_address):
    try:
        logging.info(f'Connection from {client_address[0]}:{client_address[1]}')
        
        data = b''  
        buffer_size = 1024
        while True:
            chunk = connection.recv(buffer_size)
            if not chunk:
                break
            data += chunk  
            
            if len(data) > 65536:  
                logging.error(f"[ERROR] Data size exceeds limit from {client_address[0]}:{client_address[1]}. Disconnecting.")
                break
        
        if data:
            decoded_data = data.decode('utf-8', errors='ignore')
            logging.info(f'Incoming RAW request: {decoded_data}')
    
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    
    finally:
        connection.close()

# Обработка HTTP-запросов
class DetailedHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        response_text = generate_random_string()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_text.encode('utf-8'))
        
        logging.info(f'GET request from {self.client_address[0]}:{self.client_address[1]}')
        logging.info(f'Path: {self.path}')
        logging.info(f'Headers: {self.headers}')

    def log_message(self, format, *args):
        logging.info(f'{self.client_address[0]}:{self.client_address[1]} - {format % args}')

def run_socket_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()
        logging.info(f'Socket server listening on port {port}')
        while True:
            connection, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(connection, client_address)).start()

def run_web_server(port):
    server = HTTPServer(('0.0.0.0', port), DetailedHTTPRequestHandler)
    logging.info(f'Web server listening on port {port}')
    server.serve_forever()

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py [-p PORTS] [-web PORTS]")
        sys.exit(1)
    
    options = {'-p': [], '-web': []}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in options:
            options[sys.argv[i]] = list(map(int, sys.argv[i + 1].split(',')))
            i += 2
        else:
            print("Invalid arguments")
            sys.exit(1)
    
    with ThreadPoolExecutor(max_workers=len(options['-p']) + len(options['-web'])) as executor:
        futures = []

        for port in options['-p']:
            futures.append(executor.submit(run_socket_server, port))
        
        for port in options['-web']:
            futures.append(executor.submit(run_web_server, port))
        
        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()
