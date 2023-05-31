#ifndef CHAT_ROOMS_SERVER_SERVICES_GROUPS_H
#define CHAT_ROOMS_SERVER_SERVICES_GROUPS_H

#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

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

int get_user_groups(char *req, char *res){
    char *filename = "groups.txt";
    FILE *groupsFile = fopen(filename, "r");
    if (groupsFile == NULL) {
        sprintf(error, "Could not open group file");
        sprintf(res, "ERROR %s", error);
        fclose(groupsFile);
        return -1;
    }

    char line[BUFFER_SIZE];
    char current_line[BUFFER_SIZE];
    char response_cat[BUFFER_SIZE];
    char delim[] = " ";
    strcpy(response_cat, "");

    while (fgets(line, sizeof line, groupsFile) != NULL){
        line[strcspn(line, "\r\n")] = 0;
        strcpy(current_line, line);
        
        char *ptr = strtok(line, delim);

        while(ptr != NULL)
        {
            if(strcmp(ptr, req) == 0){
               
                strcat(response_cat, current_line);
                strcat(response_cat, ":");
                break;
            }
            ptr = strtok(NULL, delim);
        }
    }
    sprintf(res, "%s", response_cat);
    return EXIT_SUCCESS;
}

int get_other_groups(char *req, char *res){
    char username[BUFFER_SIZE];
    strcpy(username, req);
    char *filename = "groups.txt";
    FILE *groupsFile = fopen(filename, "r");
    if (groupsFile == NULL) {
        sprintf(error, "Could not open group file");
        sprintf(res, "ERROR %s", error);
        fclose(groupsFile);
        return -1;
    }
    
    char line[BUFFER_SIZE];
    char current_line[BUFFER_SIZE];
    char response_cat[BUFFER_SIZE];
    char delim[] = " ";
    int flag_user;
    strcpy(response_cat, "");

    while (fgets(line, sizeof line, groupsFile) != NULL){
        line[strcspn(line, "\r\n")] = 0;
        strcpy(current_line, line);
        

        char *ptr = strtok(line, delim);
        while(ptr != NULL)
        {
            if(strcmp(ptr, username) == 0){
                flag_user = 1;
                break;
            }
            ptr = strtok(NULL, delim);
        }
        if(flag_user == 0){
            strcat(response_cat, current_line);
            strcat(response_cat, ":");
        }
        flag_user = 0;
    }

    sprintf(res, "%s", response_cat);
    return EXIT_SUCCESS;
}
#endif //CHAT_ROOMS_SERVER_SERVICES_GROUPS_H
