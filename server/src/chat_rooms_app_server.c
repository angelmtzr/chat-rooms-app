#include <unistd.h>
#include "includes/server.h"

#define PORT 5004

FILE *open_file_readmode();
FILE *open_file_appendmode();

int main() {
  Socket server = server_setup(PORT);

  while (1) {
    Socket connection = server_accept(server);

    handle_connection(server, connection, open_file_readmode(), open_file_appendmode());

    close(connection);
  }
  
}

FILE *open_file_readmode(){
  char *filename = "auth.txt";
  FILE *auth_file = fopen(filename, "r");

  return auth_file;
}

FILE *open_file_appendmode(){
  char *filename = "auth.txt";
  FILE *auth_file = fopen(filename, "a");

  return auth_file;
}
