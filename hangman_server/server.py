import socket, threading


class Player:

    def __init__(self, name, client) -> None:
        self.name = name
        self.client = client


class Server:

    host = '127.0.0.1'
    port = 7976

    def __init__(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

        self.players = []


    def broadcast(self, message):
        for player in self.players:
            player.client.send(message)


    def handle(self, player: Player):                                         
        while True:
            try:
                message = player.client.recv(1024)
                self.broadcast(message)
            except:
                self.players.remove(player)
                player.client.close()
                self.broadcast('{} left!'.format(player.name).encode('ascii'))
                break
    

    def receive(self,):
        while True:
            # add client
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))       
            client.send('NICKNAME'.encode('ascii'))
            name = client.recv(1024).decode('ascii')
            player = Player(name, client)
            self.players.append(player)

            print("Nickname is {}".format(name))
            self.broadcast("{} joined!\n".format(name).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))
            thread = threading.Thread(target=self.handle, args=(player,))
            thread.start()

