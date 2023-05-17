/**
 * @file chat_rooms_server.c
 * @author José Iván Andrade Rojas
 * @author Pablo Raschid Llamas Aun
 * @author Ángel Martínez Rodríguez
 * @author Edgar Velázquez Mercado
 * @brief This file contains the Chat Rooms Application's server. It uses TCP
 * internet sockets in order to handle and accept incoming connections from multiple clients.
 * @version 0.1
 * @date May 13, 2023
 */
#include <netinet/in.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "../includes/networking.h"
#include "../includes/encrypt.h"
#include "../includes/commons.h"

#define PORT 5000

void abort_signal_handler(int sig);
void close_all();

int server = -1, client = -1;
volatile sig_atomic_t keep_running = 1;

int main() {
  if (signal(SIGINT, abort_signal_handler) == SIG_ERR) {
    perror("[-] Error setting SIGINT signal handler");
    return EXIT_FAILURE;
  }

  InternetAddr server_addr;
  if (create_server_socket(PORT, &server, &server_addr) == -1) {
    perror("[-] Error creating server socket");
    return EXIT_FAILURE;
  }

  printf("[+] Server started. Listening on %s:%d\n",
         inet_ntoa(server_addr.sin_addr),
         ntohs(server_addr.sin_port));

  InternetAddr client_addr;
  char req[MAX_SIZE], res[MAX_SIZE];

  while (keep_running) {
    if (accept_connection(server, &client, &client_addr) == -1) {
      perror("[-] Error accepting connection from a new client");
      continue;
    }

    printf("----------------------------------------------------\n");
    printf("[+] New connection accepted from %s:%d\n",
           inet_ntoa(client_addr.sin_addr),
           ntohs(client_addr.sin_port));

    pid_t pid = fork();
    if (pid == -1) {
      perror("[-] Error creating new process");
      continue;
    }

    if (pid != 0) {
      close(client);
      continue;
    }

    if (receive_data_from(client, req) == -1) {
      perror("[-] Error receiving request from client");
      close(client);
      continue;
    }
    printf("[+] Request from client (encrypted): %s\n", req);

    caesar_decipher(req, req, CIPHER_KEY);
    printf("[+] Client request (decrypted): %s\n", req);

    if (process_request(req, res) == -1) {
      fprintf(stderr, "[-] Error processing client request: %s\n", error);
    }

    printf("[+] Server response (decrypted): %s\n", res);
    caesar_cipher(res, res, CIPHER_KEY);

    if (send_data_to(client, res) == -1) {
      perror("[-] Error sending response to client");
      close(client);
      continue;
    }
    printf("[+] Sent to client (encrypted): %s\n", res);

    close(client);
  }

  close_all();
  return EXIT_SUCCESS;
}

void abort_signal_handler(int sig) {
  printf("\n[+] Received abort signal %d\n", sig);
  printf("[+] Gracefully aborting server process...\n");
  close_all();
  exit(EXIT_SUCCESS);
}

void close_all() {
  if (client != -1) {
    close(client);
    printf("[+] Client disconnected.\n");
  }
  if (server != -1) {
    close(server);
    printf("[+] Server shut down.\n");
  }
}