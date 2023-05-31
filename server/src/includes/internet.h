#ifndef INTERNET_H
#define INTERNET_H

#include <netinet/in.h>

typedef struct sockaddr_in InternetAddress;
typedef struct sockaddr Address;
typedef int Socket;
typedef in_port_t Port;

#endif //INTERNET_H
