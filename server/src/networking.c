#include <string.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "../includes/services/auth.h"
#include "../includes/networking.h"
#include "../includes/commons.h"

int create_server_socket(in_port_t port, int *server_sock,
                         InternetAddr *server_addr) {
  int sock;
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
    return -1;
  }

  InternetAddr addr = {
      .sin_family = AF_INET,
      .sin_port = htons(port),
      .sin_addr.s_addr  = htonl(INADDR_ANY)
  };

  if (bind(sock, (Addr *) &addr, sizeof(addr)) == -1) {
    close(sock);
    return -1;
  }
  if (listen(sock, SOMAXCONN) == -1) {
    close(sock);
    return -1;
  }

  *server_addr = addr;
  *server_sock = sock;
  return EXIT_SUCCESS;
}

int accept_connection(int server_socket, int *client_sock,
                      InternetAddr *client_addr) {
  int sock;
  InternetAddr addr;
  socklen_t len = sizeof(addr);
  if ((sock = accept(server_socket, (Addr *) &addr, &len)) == -1) {
    return -1;
  }
  *client_addr = addr;
  *client_sock = sock;
  return EXIT_SUCCESS;
}

int receive_data_from(int connection, char *data) {
  ssize_t bytes_read;
  if ((bytes_read = recv(connection, data, MAX_SIZE - 1, 0)) == -1) {
    return -1;
  }
  data[bytes_read] = '\0';
  return EXIT_SUCCESS;
}

int send_data_to(int connection, char *data) {
  if (send(connection, data, strlen(data), 0) == -1) {
    return -1;
  }
  return EXIT_SUCCESS;
}

int process_request(char *req, char *res) {
  char *service = strsep(&req, " ");
  printf("[+] Service requested: %s\n", service);
  if (strcmp(service, "auth") == 0) {
    char token[MAX_SIZE];
    if (auth(req, token) == -1) {
      sprintf(res, "ERROR %s", error);
      return -1;
    }
    printf("[+] Authenticated successfully\n");
    sprintf(res, "SUCCESS token=%s", token);
  } /*else if (strcmp(service, "new_group") == 0) {
    char token[MAX_SIZE];
    if (new_group(req, token) == -1) {
      fprintf(stderr, "[-] New group error: %s\n", error);
      sprintf(res, "ERROR %s", error);
      return -1;
    }
    printf("[+] New group created\n");
    sprintf(res, "SUCCESS token=%s", token);
  }*/
  else {
    printf(error, "Requested an invalid service");
    sprintf(res, "ERROR %s", error);
    return -1;
  }
  return EXIT_SUCCESS;
}





