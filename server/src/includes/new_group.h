#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifndef CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H
#define CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H

#include "commons.h"
#include "server.h"

#define BUFFER_SIZE 1024

int new_group_service(char *req, char *res){
    
    if (req == NULL) {
        sprintf(error, "The username or the group name is missing");
        sprintf(res, "ERROR %s", error);
        return -1;
    }

    char *filename = "groups.txt";
    FILE *groupsFile = fopen(filename, "a");
    if (groupsFile == NULL) {
        sprintf(error, "Could not open group file");
        sprintf(res, "ERROR %s", error);
        fclose(groupsFile);
        return -1;
    }

    fprintf(groupsFile, "%s\n", req);
    fclose(groupsFile);
    printf("[+] New group created successfully\n");
    sprintf(res, "SUCCESS Group created successfully");
    return EXIT_SUCCESS;
}
#endif //CHAT_ROOMS_SERVER_SERVICES_NEW_GROUP_H
