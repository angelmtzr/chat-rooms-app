# Chat Rooms App

## Table of Contents

- [Description](#description)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

## Description

This project is a distributed chat application that enables users to communicate with each other through chatrooms.
The server is implemented in C, while the clients are implemented in Python. The communication between the server and
clients is established through sockets.

The application allows users to authenticate with a username and password, after which they can create or join
chatrooms. Once inside a chatroom, users can send and receive messages from other users in the same chatroom.

The distributed nature of this application allows for scalability and fault tolerance. The server can be run on multiple
machines, with each machine handling a portion of the total load. In case of server failure, the remaining servers can
continue to handle the load, ensuring that the application remains available.

The client provides a friendly GUI built using the Python library
[CustomTkinter](https://customtkinter.tomschimansky.com/) in a way that users may interact with the server and other
users, with graphical elements such as text boxes and buttons. The server manages the creation and deletion of
chatrooms, as well as the authentication of users.


## Getting Started

First, clone the GitHub repository:
```bash
git clone https://github.com/angelmtzr/chat-rooms-app.git
```

Then, navigate to the project directory:
```bash
cd chat-rooms-app
```

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue on the GitHub repository.
If you want to contribute code, please fork the repository and submit a pull request.
