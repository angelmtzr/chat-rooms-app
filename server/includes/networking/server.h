#ifndef SERVER_H
#define SERVER_H

#include "internet.h"

#define BUFFER_SIZE 1024
#define CIPHER_KEY 14
#define TOKEN_SIZE 30

/**
 * @brief Creates a TCP socket for the server and binds it to
 * the given port so that it can listen for connections.
 *
 * @param[in] port The port the server will bind and listen to.
 * @return The newly created socket.
 */
Socket server_setup(Port port);
/**
 * @brief Lets the server accept new connections from incoming clients.
 *
 * @param[in] server The server.
 * @return The newly accepted client connection.
 */
Socket server_accept(Socket server);
/**
 * @brief Handles the processing of the the new client connection.
 *
 * The function creates a new process to handle the new connection and lets
 * the main process return and continue accepting new connections. The request
 * from the client is received and decrypted. Then the request is processed.
 * And at last it sends a response to the client. The closing of the server
 * and client connection is handled properly.
 *
 * @param[in] server The server.
 * @param[in] client The client connection.
 */
void handle_connection(Socket server, Socket client);

#endif //SERVER_H
