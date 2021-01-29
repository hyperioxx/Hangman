import socket 

class Client:
    
    def __init__(self, name):
        self.name = name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 7976))


    def receive(self):
        while True: 
            print("in receive")                                                
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICKNAME':
                    self.client.send(self.name.encode('ascii'))
                else:
                    print(message)
            except:                                                
                print("An error occured!")
                self.client.close()
                break


    def write(self):
        while True:
            print("in write")                                                
            message = input(" ")
            self.client.send(message.encode('ascii'))