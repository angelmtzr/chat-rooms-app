cmake_minimum_required(VERSION 3.25)
project(server C)

set(CMAKE_C_STANDARD 23)

add_executable(chat_rooms_server src/main.c src/networking.c includes/networking.h src/services/auth.c includes/services/auth.h src/encrypt.c includes/encrypt.h includes/commons.h src/services/new_group.c includes/services/new_group.h)
