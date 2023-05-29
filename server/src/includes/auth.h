#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>


#ifndef AUTH_H
#define AUTH_H

#include "commons.h"
#include "server.h"

#define TOKEN_SIZE 30
#define BUFFER_SIZE 1024

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

int read_database(char *req, char *res, FILE *auth_file){

  char *reqUsername = strsep(&req, " ");
  char *reqPassword = strsep(&req, " ");

  if (reqUsername == NULL || reqPassword == NULL) {
    sprintf(error, "The username or password is missing");
    sprintf(res, "ERROR %s", error);
    return -1;
  }

  if (auth_file == NULL) {
    sprintf(error, "Could not open file");
    sprintf(res, "ERROR %s", error);
    return -1;
  }

  char line[BUFFER_SIZE];
  char username[BUFFER_SIZE];
  char password[BUFFER_SIZE];

  while (fgets(line, sizeof line, auth_file) != NULL){
    line[strcspn(line, "\r\n")] = 0;
    char *ptr = strtok(line, " ");
    if (ptr != NULL) {
      strncpy(username, ptr, BUFFER_SIZE);
      ptr = strtok(NULL, " ");

      if (ptr != NULL) {
        strncpy(password, ptr, BUFFER_SIZE);
      }
    }
    if(strcmp(username, reqUsername) == 0 &&
       strcmp(password, reqPassword) == 0) {
         return EXIT_SUCCESS; 
    }
  }
  sprintf(error, "The username or password is wrong");
  sprintf(res, "ERROR %s", error);
  return -1;
}

int write_database(char *req, char *res, FILE *auth_file){

  if (req == NULL) {
    sprintf(error, "The username or password is missing");
    sprintf(res, "ERROR %s", error);
    return -1;
  }

  if (auth_file == NULL) {
    sprintf(error, "Could not open file");
    sprintf(res, "ERROR %s", error);
    return -1;
  }

  fprintf(auth_file, "%s\n", req);
  return EXIT_SUCCESS;
}

int auth_service(char *req, char *res, FILE *auth_file) {

  if (read_database(req, res, auth_file) == -1) {
    return -1;
  }
  printf("[+] Authenticated successfully\n");
  char *token = generate_token(TOKEN_SIZE);
  sprintf(res, "SUCCESS token=%s", token);
  free(token);
  return EXIT_SUCCESS;
}

int new_user_service(char *req, char *res, FILE *auth_file){
  if (write_database(req, res, auth_file) == -1){
    return -1;
  }
  printf("[+] New user created successfully\n");
  sprintf(res, "SUCCESS User created successfully");
  return EXIT_SUCCESS;
}

#endif //AUTH_H
