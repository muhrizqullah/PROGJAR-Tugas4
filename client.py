import socket
import pickle

SERVER_ADDRESS = "127.0.0.1"
PORT = 2707
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"
class TicTacToe:
    
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = None
        self.opponent = None
        self.winner = None
        self.game_over = False
        
        self.counter = 0
        
    def connectToServer(self, host, port):
        server_address = (host, port)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(server_address)
        
        self.handleConnection(client_socket)
        
    def handleConnection(self, client_socket):
        name = input("Enter name: ")
        client_socket.send(name.encode('utf-8'))
        
        response = client_socket.recv(BUFFER_SIZE)
         
        u = pickle.loads(response)
        
        self.you = u.get('symbol')
        
        if self.you == "X":
            turn = "Player 1"
            self.opponent = "O"
        else:
            turn = "Player 2"
            self.opponent = "X"
            
        print(f"Hello {name}! You are {turn}, you're opponent is {u.get('opponent')}")
            
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row, column): ")
                move = move.split(', ')
                if self.isValidMove(move):
                    p = pickle.dumps(move)
                    client_socket.send(p)
                    self.applyMove(move, self.you)
                    self.turn = self.opponent
                else:
                    print("Invalid Move!")
                    
            else:
                data = client_socket.recv(BUFFER_SIZE)
                u = pickle.loads(data)
                if not data:
                    break
                else:
                    self.applyMove(u,self.opponent)
                    self.turn = self.you

        client_socket.close()
    
    def applyMove(self, move, player):
        if self.game_over:
            return
        else:
            self.counter += 1
            self.board[int(move[0])][int(move[1])] = player
            self.printBoard()
            
            if self.isWon():
                if self.winner == self.you:
                    print("Winner!")
                    exit()
                elif self.winner ==self.opponent:
                    print("Loser!")
                    exit()
            else:
                if self.counter == 9:
                    print("Tie!")
                    exit()
            
    def isValidMove(self, move):
        return self.board[int(move[0])][int(move[1])] == " "
    
    def isWon(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
            
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True

        return False
                    
    def printBoard(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("----------")

    
game = TicTacToe()
game.connectToServer(SERVER_ADDRESS, PORT)