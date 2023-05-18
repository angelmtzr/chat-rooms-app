#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifndef AUTH_H
#define AUTH_H

#include "commons.h"
#include "server.h"

#define TOKEN_SIZE 30

char *generate_token(size_t token_size) {
  char *token = malloc(token_size * sizeof(char));
  static const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  srand((unsigned int) time(NULL)); // NOLINT(cert-msc51-cpp)
  for (int i = 0; i < token_size; i++) {
    token[i] = charset[rand() % (sizeof(charset) - 1)]; // NOLINT(cert-msc50-cpp)
  }
  token[token_size] = '\0';
  return token;
}

int auth_service(char *req, char *res) {
  char *username = strsep(&req, " ");
  char *password = strsep(&req, " ");
  if (username == NULL || password == NULL) {
    sprintf(error, "The username or password is missing");
    sprintf(res, "ERROR %s", error);
    return -1;
  }
  // TODO: Have this come from database
  if (strcmp(username, "username") != 0 ||
      strcmp(password, "password") != 0) {
    sprintf(error, "The username or password is wrong");
    sprintf(res, "ERROR %s", error);
    return -1;
  }
  printf("[+] Authenticated successfully\n");
  char *token = generate_token(TOKEN_SIZE);
  sprintf(res, "SUCCESS token=%s", token);
  free(token);
  return EXIT_SUCCESS;
}

#endif //AUTH_H
