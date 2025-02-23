"""
Author: [Your Name]
Program: Chat Client
Description: A simple chat client that connects to a chat server, allows users to join rooms, 
set nicknames, send/receive messages, list users, and logout.
"""

import socket
import select
import sys

# Server details
SERVER_IP = "104.197.153.180"
SERVER_PORT = 41400
BUFFER_SIZE = 1024


def connect_to_server():
    """Establishes a connection to the chat server."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print(f"Connected to chat server at {SERVER_IP}:{SERVER_PORT}")
        return client_socket
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)


def get_room_list(client_socket):
    """Requests and displays the list of available chat rooms."""
    client_socket.sendall("/list".encode())
    raw_data = client_socket.recv(BUFFER_SIZE).decode().strip()

    if not raw_data.isdigit():  # Handle unexpected responses
        print(f" Server returned an invalid response: '{raw_data}'")
        return

    room_count = int(raw_data)
    if room_count == 0:
        print("No chat rooms available.")
    else:
        print("Available chat rooms:")
        for _ in range(room_count):
            room_name = client_socket.recv(BUFFER_SIZE).decode().strip()
            print(f"- {room_name}")


def join_room(client_socket):
    """Allows the user to join or create a chat room."""
    while True:
        room_name = input("Enter a room name to join (or create): ").strip()
        if not room_name:
            print("Room name cannot be empty.")
            continue

        client_socket.sendall(f"/join {room_name}".encode())
        response = client_socket.recv(BUFFER_SIZE).decode().strip()

        if response == "0":
            print(f"Joined room: {room_name}")
            return room_name
        elif response == "1":
            print("Invalid room name format. Try again.")
        else:
            print("Unexpected server response. Try again.")


def set_nickname(client_socket):
    """Prompts for and set a unique nickname."""
    while True:
        nickname = input("Enter your nickname: ").strip()
        if not nickname:
            print("Nickname cannot be empty.")
            continue

        client_socket.sendall(f"/nick {nickname}".encode())
        response = client_socket.recv(BUFFER_SIZE).decode().strip()

        if response == "0":
            print(f"Nickname set to: {nickname}")
            return
        elif response == "1":
            print("Invalid nickname format. Try again.")
        elif response == "2":
            print("Nickname already taken. Choose another.")
        else:
            print("Unexpected server response. Try again.")


def list_users(client_socket):
    """Shows who's in the chat rooms."""
    client_socket.sendall("/who".encode())
    print("Users in the room:")
    while True:
        user = client_socket.recv(BUFFER_SIZE).decode().strip()
        if not user:
            break
        print(f"- {user}")


def chat(client_socket):
    """So you can....chat in the chat room."""
    print("You are now in the chat. Type your messages and press Enter to send.")
    print("Type '/who' to list users or '/logout' to exit.")

    while True:
        reads, _, _ = select.select([client_socket, sys.stdin], [], [])

        for source in reads:
            if source == client_socket:
                message = client_socket.recv(BUFFER_SIZE).decode().strip()
                if not message:
                    print("Disconnected from the server.")
                    client_socket.close()
                    sys.exit(0)
                print(message)  # Display incoming message
            elif source == sys.stdin:
                user_message = sys.stdin.readline().strip()
                if user_message.lower() == "/logout":
                    client_socket.sendall("/logout".encode())
                    print("You have logged out.")
                    client_socket.close()
                    sys.exit(0)
                elif user_message.lower() == "/who":
                    list_users(client_socket)
                else:
                    client_socket.sendall(user_message.encode())  # Send user message to server


def main():
    """Main function to run the chat client."""
    client_socket = connect_to_server()

    while True:
        action = input("\nType '/list' to see available rooms or '/join ROOM' to enter a chat room: ").strip()
        if action == "/list":
            get_room_list(client_socket)
        elif action.startswith("/join "):
            room_name = action.split("/join ", 1)[1].strip()
            if room_name:
                client_socket.sendall(f"/join {room_name}".encode())
                response = client_socket.recv(BUFFER_SIZE).decode().strip()
                if response == "0":
                    print(f"Joined room: {room_name}")
                    break
                else:
                    print("Invalid room name. Try again.")
        else:
            print("Invalid command. Try again.")

    set_nickname(client_socket)
    chat(client_socket)


if __name__ == "__main__":
    main()
