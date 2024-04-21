import socket
import threading

# Game variables
board = ["-"] * 9
current_player = "X"


# Function to display the game board
def display_board():
    print("-------------")
    for i in range(0, 9, 3):
        print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
        print("-------------")


# Function to handle client connections
def handle_client(client_socket, player):
    global current_player

    client_socket.send(
        "Welcome to Tic-Tac-Toe! Waiting for other players to join...\n".encode()
    )

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        print(f"Received move from player {player}: {data}")

        # Process player's move
        move = int(data)
        if board[move] == "-":
            board[move] = current_player
            display_board()

            # Check for win or draw
            if check_win() or check_draw():
                break

            # Switch player
            current_player = "O" if current_player == "X" else "X"
            client_socket.send(f"Waiting for {current_player}'s move...\n".encode())
        else:
            client_socket.send("Invalid move. Try again.\n".encode())

    client_socket.close()


# Function to check for a win
def check_win():
    # Check rows, columns, and diagonals
    return (
        board[0] == board[1] == board[2] != "-"
        or board[3] == board[4] == board[5] != "-"
        or board[6] == board[7] == board[8] != "-"
        or board[0] == board[3] == board[6] != "-"
        or board[1] == board[4] == board[7] != "-"
        or board[2] == board[5] == board[8] != "-"
        or board[0] == board[4] == board[8] != "-"
        or board[2] == board[4] == board[6] != "-"
    )


# Function to check for a draw
def check_draw():
    return "-" not in board


# Set up server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 65432))
server_socket.listen(1)

print("Server is listening...")

# Wait for players to connect
player_number = 0
while True:
    client_socket, client_address = server_socket.accept()
    player_number += 1
    print(f"Player {player_number} connected from {client_address}")

    # Start a new thread to handle the player
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, player_number)
    )
    client_thread.start()

    # Start the game when two players are connected
    if player_number == 2:
        break
