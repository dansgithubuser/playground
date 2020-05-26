import SimpleWebSocketServer as swss

class Socket(swss.WebSocket):
    def handleMessage(self):
        try:
            print(self.data)
        except Exception as e:
            print(e)

class Server(swss.SimpleWebSocketServer):
    def __init__(self, *args, **kwargs):
        swss.SimpleWebSocketServer.__init__(self, *args, **kwargs)

    def send(self, message):
        for i in self.connections.values():
            i.sendMessage(message)

server = Server('0.0.0.0', 8000, Socket)

while True:
    invocation = input()
    try:
        split = invocation.split()
        if not split or split[0] == 'serve':
            server.serveonce()
        elif split[0] == 'send':
            server.send(invocation.split(' ', 1)[1])
    except Exception as e:
        print(e)
