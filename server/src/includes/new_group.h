#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifndef CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H
#define CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H

#include "commons.h"
#include "server.h"

#define BUFFER_SIZE 1024

int new_group_service(char *req, char *res){
    char *reqUsername = strsep(&req, " ");
    char *reqGroupName = strsep(&req, " ");

    if (reqUsername == NULL || reqGroupName == NULL) {
        sprintf(error, "The username or the group name is missing");
        sprintf(res, "ERROR %s", error);
        return -1;
    }

    char usersFileName[BUFFER_SIZE];
    char conversationFileName[BUFFER_SIZE];

    strcpy(usersFileName, reqGroupName);
    strcat(usersFileName, ".users");

    strcpy(conversationFileName, reqGroupName);
    strcat(conversationFileName, ".conv");

    FILE *usersFile = fopen(usersFileName, "a");
    FILE *conversationFile = fopen(conversationFileName, "a");

    if (usersFile == NULL) {
        sprintf(error, "Could not open group users file");
        sprintf(res, "ERROR %s", error);
        return -1;
    }
    if (conversationFile == NULL) {
        sprintf(error, "Could not open group conversation file");
        sprintf(res, "ERROR %s", error);
        return -1;
    }
    
    fprintf(usersFile, "%s\n", reqUsername);
    fclose(usersFile);
    fclose(conversationFile);
    printf("[+] New user created successfully\n");
    sprintf(res, "SUCCESS Group created successfully");
    return EXIT_SUCCESS;
}
#endif //CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H
