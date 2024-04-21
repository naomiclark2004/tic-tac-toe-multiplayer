import socket


# Function to display the game board
def display_board(board):
    print("-------------")
    for i in range(0, 9, 3):
        print(f"| {board[i]} | {board[i+1]} | {board[i+2]} |")
        print("-------------")


# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 65432))

# Receive welcome message
print(client_socket.recv(1024).decode())

# Main game loop
while True:
    # Display current board state
    board_state = client_socket.recv(1024).decode()
    print(board_state)
    if "Waiting" not in board_state:
        display_board(board_state.split("\n")[1:-1])

    # Get player's move
    move = input("Enter your move (0-8): ")
    client_socket.send(move.encode())

    # Check for game over
    response = client_socket.recv(1024).decode()
    print(response)
    if "win" in response or "draw" in response:
        break

# Close connection
client_socket.close()
