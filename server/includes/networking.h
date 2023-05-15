#ifndef CHAT_ROOMS_SERVER_NETWORKING_H
#define CHAT_ROOMS_SERVER_NETWORKING_H

#include <arpa/inet.h>
#include <sys/socket.h>

#define CIPHER_KEY 14


typedef struct sockaddr_in InternetAddr;
typedef struct sockaddr Addr;

int create_server_socket(in_port_t port, int *server_sock,
                         InternetAddr *server_addr);
int accept_connection(int server_socket, int *client_sock,
                      InternetAddr *client_addr);
int receive_data_from(int connection, char *data);
int send_data_to(int connection, char *data);
int process_request(char *req, char *res);

#endif //CHAT_ROOMS_SERVER_NETWORKING_H
