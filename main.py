import socketserver
from Analysis import Analysis

SERVER_HOST = '172.20.10.6'
SERVER_PORT = 9000
BUF_SIZE = 2048


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(BUF_SIZE)
        data = data.decode()
        print(data)
        analysis_data = Analysis().analysis(data)
        print(str(analysis_data).encode())
        self.request.send(str(analysis_data).encode())
        return


class ForkingServer(socketserver.ThreadingMixIn, socketserver.TCPServer, ):
    pass


def main():
    server = ForkingServer((SERVER_HOST, SERVER_PORT), ForkingServerRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
