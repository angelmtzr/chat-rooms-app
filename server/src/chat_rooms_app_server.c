#include <unistd.h>
#include "../includes/networking/server.h"

#define PORT 5000

int main() {
  Socket server = server_setup(PORT);

  while (1) {
    Socket connection = server_accept(server);

    handle_connection(server, connection);

    close(connection);
  }
}
