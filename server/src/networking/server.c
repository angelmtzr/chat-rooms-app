#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include "../../includes/networking/server.h"
#include "../../includes/services/auth.h"
#include "../../includes/networking/encrypt.h"
#include "../../includes/commons.h"
#include "../../includes/networking/process.h"

Socket server_setup(Port port) {
  Socket server;
  if ((server = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
    perror("[-] Error creating server socket");
    exit(EXIT_FAILURE);
  }

  InternetAddress server_address = {
      .sin_family = AF_INET,
      .sin_addr.s_addr  = INADDR_ANY,
      .sin_port = htons(port)
  };

  if (bind(server, (Address *) &server_address, sizeof(server_address)) == -1) {
    perror("[-] Error binding socket");
    close(server);
    printf("[-] Server shut down.");
    printf("----------------------------------------------------\n");
    exit(EXIT_FAILURE);
  }

  if (listen(server, SOMAXCONN) == -1) {
    perror("[-] Error in socket listen");
    close(server);
    printf("[-] Server shut down.");
    printf("----------------------------------------------------\n");
    exit(EXIT_FAILURE);
  }

  printf("----------------------------------------------------\n");
  printf("[+] Server started. Listening from %s:%d...\n",
         inet_ntoa(server_address.sin_addr),
         ntohs(server_address.sin_port));
  printf("----------------------------------------------------\n");
  return server;
}

Socket server_accept(Socket server) {
  int client;
  InternetAddress client_address;
  socklen_t client_address_length = sizeof(client_address);
  if ((client = accept(server, (Address *) &client_address, &client_address_length)) == -1) {
    perror("[-] Error accepting connection from a new client");
    printf("----------------------------------------------------\n");
    exit(EXIT_FAILURE);
  }
  printf("[+] New connection accepted from %s:%d\n",
         inet_ntoa(client_address.sin_addr),
         ntohs(client_address.sin_port));
  return client;
}

int process_request(char *req, char *res) {
  char *service = strsep(&req, " ");
  printf("[+] Service requested: %s\n", service);

  if (strcmp(service, "auth") == 0) {
    if (auth_service(req, res) == -1) {
      return -1;
    }
  }
    /*else if (strcmp(service, "new_group") == 0) {
      if (new_group_service(req, res) == -1) {
        return -1;
      }
    }*/
  else {
    sprintf(error, "Requested an invalid service");
    sprintf(res, "ERROR %s", error);
    return -1;
  }
  return EXIT_SUCCESS;
}

void handle_connection(Socket server, Socket client) {
  ProcessId process_id = create_new_process();

  if (is_main_process(process_id)) {
    close(client);
    return;
  }

  close(server); // Server socket is no longer needed here

  // Receives the request from the client (encrypted)
  char encrypted_request[BUFFER_SIZE];
  ssize_t bytes_read;
  if ((bytes_read = recv(client, encrypted_request, sizeof(encrypted_request) - 1, 0)) == -1) {
    perror("[-] Error receiving request from client");
    close(client);
    fprintf(stderr, "[-] Client connection closed.\n");
    printf("----------------------------------------------------\n");
    exit(EXIT_FAILURE);
  }
  encrypted_request[bytes_read] = '\0';
  printf("----------------------------------------------------\n");
  // Decrypts the client request
  printf("[+] Client sent (encrypted): %s\n", encrypted_request);
  char *decrypted_request = caesar_decipher(encrypted_request, CIPHER_KEY);
  printf("[+] Client request (decrypted): %s\n", decrypted_request);

  // Processes accordingly the client request
  char decrypted_response[BUFFER_SIZE];
  if (process_request(decrypted_request, decrypted_response) == -1) {
    fprintf(stderr, "[-] Error processing client request: %s\n", error);
  }
  free(decrypted_request);

  // Encrypt server response
  printf("[+] Server response (decrypted): %s\n", decrypted_response);
  char *encrypted_response = caesar_cipher(decrypted_response, CIPHER_KEY);
  printf("[+] Server sent (encrypted): %s\n", decrypted_response);

  // Send response to client
  if (send(client, encrypted_response, strlen(encrypted_response), 0) == -1) {
    perror("[-] Error sending response to client");
    close(client);
    perror("[-] Client connection closed.");
    printf("----------------------------------------------------\n");
    exit(EXIT_FAILURE);
  }
  free(encrypted_response);
  close(client);
  printf("[+] Client connection closed.\n");
  printf("----------------------------------------------------\n");
  exit(EXIT_SUCCESS);
}