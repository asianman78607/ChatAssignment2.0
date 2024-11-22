import socket
import threading
import tkinter as tk
from subprocess import Popen

# Server details
HOST = '127.0.0.1'
PORT = 12345
clients = {}
server_socket = None
server_running = False


def broadcast(message, sender_socket):
    """Send message to all connected clients except the sender."""
    for client_socket in clients.keys():
        if client_socket != sender_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[client_socket]


def handle_client(client_socket):
    """Handle messages from a single client."""
    try:
        # Get the username from the client
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        print(f"{username} has joined the chat!")
        broadcast(f"{username} has joined the chat!".encode('utf-8'), client_socket)

        # Receive and broadcast messages
        while True:
            message = client_socket.recv(1024)
            if message:
                formatted_message = f"{clients[client_socket]}: {message.decode('utf-8')}"
                print(formatted_message)
                broadcast(formatted_message.encode('utf-8'), client_socket)
            else:
                break
    except:
        pass
    finally:
        print(f"{clients[client_socket]} has left the chat.")
        broadcast(f"{clients[client_socket]} has left the chat.".encode('utf-8'), client_socket)
        client_socket.close()
        del clients[client_socket]


def start_server(add_client_button, start_button, stop_button):
    """Start the chat server."""
    global server_socket, server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    server_running = True

    # Enable/Disable buttons
    add_client_button.config(state=tk.NORMAL)
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

    # Accept clients in a separate thread
    threading.Thread(target=accept_clients, args=(server_socket,), daemon=True).start()


def stop_server(add_client_button, start_button, stop_button):
    """Stop the chat server."""
    global server_socket, server_running
    if server_running:
        server_running = False
        server_socket.close()
        print("Server stopped.")

        # Enable/Disable buttons
        add_client_button.config(state=tk.DISABLED)
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

