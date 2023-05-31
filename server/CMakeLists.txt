cmake_minimum_required(VERSION 3.25)
project(server C)

set(CMAKE_C_STANDARD 23)

add_executable(chat_rooms_server src/services/auth.c includes/services/auth.h src/networking/encrypt.c includes/networking/encrypt.h includes/commons.h src/services/new_group.c includes/services/new_group.h src/chat_rooms_app_server.c includes/networking/process.h includes/networking/server.h src/networking/server.c includes/networking/internet.h src/networking/process.c)
