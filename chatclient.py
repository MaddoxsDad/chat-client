import socket
import select
import sys

# Kevin Landry
# CPSC 414
# Chat Client
# Purpose: Purpose: A simple command-line chat client that connects to a remote chat server, allowing users 
# to list, join, and create chat rooms. It uses non-blocking input handling to ensure smooth 
# communication and follows best practices (as far as I can tell) for socket programming.
#
# Honor Pledge: "I have neither given nor received unauthorized aid on this assignment."

# Server details
SERVER_IP = "104.197.153.180"
SERVER_PORT = 41400

def connect_to_server():
    """ Establish a connection to the chat server. """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to chat server at {SERVER_IP}:{SERVER_PORT}")
        return client_socket
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

def list_rooms(sock):
    """ Request a list of chat rooms from the server. """
    sock.sendall("/list\n".encode())
    try:
        room_count = int(sock.recv(1024).decode().strip())
        print(f"Number of available rooms: {room_count}")
        for _ in range(room_count):
            room_name = sock.recv(1024).decode().strip()
            print(f" - {room_name}")
    except Exception as e:
        print(f"Error retrieving room list: {e}")

def join_room(sock):
    """ Allow user to join or create a chat room. """
    while True:
        room_name = input("Enter the room name to join (or create a new one): ")
        sock.sendall(f"/join {room_name}\n".encode())
        response = sock.recv(1024).decode().strip()
        if response == "0":
            print(f"Successfully joined room: {room_name}")
            return True
        else:
            print("Invalid room name format. Try again.")

def set_nickname(sock):
    """ Allow user to choose a nickname. """
    while True:
        nickname = input("Enter a nickname: ")
        sock.sendall(f"/nick {nickname}\n".encode())
        response = sock.recv(1024).decode().strip()
        if response == "0":
            print(f"Nickname set to {nickname}")
            return True
        elif response == "2":
            print("Nickname is already taken. Choose another one.")
        else:
            print("Invalid nickname format. Try again.")

def chat_loop(sock):
    """ Handle chat interaction between user and server. """
    print("\n[ You are now in the chatroom! Type messages to chat. ]")
    print("[ Type '/who' to see who is online, or '/logout' to exit. ]\n")

    while True:
        reads, _, _ = select.select([sock, sys.stdin], [], [])
        
        for source in reads:
            if source == sock:
                message = sock.recv(1024).decode().strip()
                if not message:
                    print("Disconnected from server.")
                    return
                print(message)
            else:
                user_input = sys.stdin.readline().strip()
                sock.sendall(f"{user_input}\n".encode())
                
                if user_input == "/logout":
                    print("Logging out...")
                    sock.close()
                    return

def main():
    sock = connect_to_server()

    while True:
        action = input("Type '/list' to see chat rooms or '/join [room_name]' to enter a room: ")
        if action == "/list":
            list_rooms(sock)
        elif action.startswith("/join"):
            sock.sendall(f"{action}\n".encode())
            if join_room(sock):
                break
        else:
            print("Invalid command. Please use '/list' or '/join [room_name]'.")

    if set_nickname(sock):
        chat_loop(sock)

if __name__ == "__main__":
    main()
