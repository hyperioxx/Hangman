from hangman_server.server import Player
from itertools import cycle
import socket
import threading
import multiprocessing
from hangman_server.words import WordFactory


class Game:

    GUESSES = 6
    HOST = '127.0.0.1'
    PORT = 7976

    def __init__(self) -> None:
        self._running = True
        self.word = WordFactory.build()
        # self.players = self.player_setup()
        self.players = []
      

        # Server Setup
        self.host = '127.0.0.1'
        self.port = 7976
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()

    # @staticmethod
    # def player_setup() -> list:
    #     player_list = []
    #     while True:
    #         num_players = input("How many players? ")
    #         try:
    #             num_players = int(num_players)
    #             assert num_players > 0
    #             break
    #         except: 
    #             print("Input must be an Integer > 0")
        
    #     for i in range(num_players):
    #        username =  input("Player {}, please enter your username: ".format(i + 1))
    #        # TODO checks for empty name
    #        player_list.append(username)
    
    #     return player_list


    def broadcast(self, message, player):
        # for player in self.players:
        print("broadcasting ", message)
        player.client.send(message.encode("ascii"))


    def start(self, player: Player) -> None:
        # for player in cycle(self.players):
        while True:
            print("in start")
            try:
                self.broadcast("{}: Guess a character or a word? ".format("P1"), player)
                string = player.client.recv(1024)
                self.broadcast(string)

                if self.is_word(string):
                    check = self.word.guess_word(string)
                    if check:
                        self.broadcast("{}: You've Won the Game!".format("P1"))
                        break
                else:
                    check = self.word.guess(string)

                if self.word.incorrect_guesses_count >= Game.GUESSES:
                    self.broadcast("You've Lost :(")
                    break
                self.broadcast(check)
                self.broadcast(self.word)
            except:
                self.players.remove(player)
                player.client.close()
                self.broadcast('{} left!'.format(player.name).encode('ascii'))
                break
            

    def receive(self):
        while True:
            # add client
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))       
            client.send('NICKNAME'.encode('ascii'))
            name = client.recv(1024).decode('ascii')
            player = Player(name, client)
            self.players.append(player)
            print("Nickname is {}".format(name))
            self.broadcast("{} joined!\n".format(name).encode('ascii'), player)
            client.send('Connected to server!'.encode('ascii'))
            thread = multiprocessing.Process(target=self.start, args=(player,))
            thread.start()

    @staticmethod
    def is_word(s: str) -> bool:
        if len(s) > 1 :
            return True
        return False