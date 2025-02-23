import select
import sys

# Chat Client - Rushing to finish this before the deadline.
# Connects to the chat server, lets me join rooms, pick a nickname, and chat.
# No extra fluff, just what’s required.

SERVER_IP = "104.197.153.180"
SERVER_PORT = 41400

def connect_to_server():
    """ Connect to the chat server. """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to chat server at {SERVER_IP}:{SERVER_PORT}")
        return client_socket
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

def list_rooms(sock):
    """ Ask for the list of rooms. """
    sock.sendall("/list\n".encode())
    try:
        room_count = int(sock.recv(1024).decode().strip())  # Get number of rooms
        print(f"Number of available rooms: {room_count}")
        for _ in range(room_count):
            print(f" - {sock.recv(1024).decode().strip()}")  # Print each room name
    except Exception as e:
        print(f"Error retrieving room list: {e}")

def join_room(sock):
    """ Join a room. If invalid, keep asking. """
    while True:
        room_name = input("Enter the room name to join (or create a new one): ")
        sock.sendall(f"/join {room_name}\n".encode())
        response = sock.recv(1024).decode().strip()
        if response == "0":
            print(f"Joined room: {room_name}")
            return True
        else:
            print("Invalid room name. Try again.")

def set_nickname(sock):
    """ Pick a nickname. Keep trying if taken or invalid. """
    while True:
        nickname = input("Enter a nickname: ")
        sock.sendall(f"/nick {nickname}\n".encode())
        response = sock.recv(1024).decode().strip()
        if response == "0":
            print(f"Nickname set to: {nickname}")
            return True
        elif response == "2":
            print("Nickname already taken. Try another.")
        else:
            print("Invalid nickname format. Try again.")

def chat_loop(sock):
    """ Core chat functionality. Send/receive messages. """
    print("\n[ In the chatroom. Type messages to chat. ]")
    print("[ Use '/who' to list users or '/logout' to exit. ]\n")

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
            print("Invalid command. Use '/list' or '/join [room_name]'.")
    
    if set_nickname(sock):
        chat_loop(sock)

if __name__ == "__main__":
    main()