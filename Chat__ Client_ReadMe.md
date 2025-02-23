# Chat Client

## Overview
This is a simple command-line chat client that connects to a remote chat server at `104.197.153.180:41400`. 
It allows users to list available chat rooms, join or create a room, and chat with others in real time. 
The client uses Python's `select` module to handle both user input and server messages simultaneously, 
ensuring smooth, non-blocking communication.

## Features/Requirements
- Connects to the chat server and lists available rooms (`/list`).
- Joins an existing room or creates a new one (`/join ROOM_NAME`).
- Allows users to pick a unique nickname (`/nick NAME`).
- Sends and receives messages in real time.
- Lists active users in the chat room (`/who`).
- Supports clean disconnection with `/logout`.

## Usage
1. **Run the program**  
   bash
   python3 chat_client.py