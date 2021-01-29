from hangman_server import Game


class App:

    @staticmethod
    def run():
        game = Game()
        game.receive()


if __name__ == '__main__':
    App.run()


