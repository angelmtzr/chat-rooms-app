#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../../includes/commons.h"
#include "../../includes/services/auth.h"

void generate_token(char *token) {
  static const char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  srand((unsigned int) time(NULL)); // NOLINT(cert-msc51-cpp)
  for (int i = 0; i < TOKEN_SIZE; i++) {
    token[i] = charset[rand() % (sizeof(charset) - 1)]; // NOLINT(cert-msc50-cpp)
  }
  token[TOKEN_SIZE] = '\0';
}

int auth(char *params, char *token) {
  char *username = strsep(&params, " ");
  char *password = strsep(&params, " ");
  if (username == NULL || password == NULL) {
    sprintf(error, "The username or password is missing");
    return -1;
  }
  if (strcmp(username, USERNAME) != 0 ||
      strcmp(password, PASSWORD) != 0) {
    sprintf(error, "The username or password is wrong");
    return -1;
  }
  generate_token(token);
  return EXIT_SUCCESS;
}

