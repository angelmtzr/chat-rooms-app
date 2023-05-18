#include "../../includes/networking/process.h"

int is_main_process(ProcessId id) {
  return id > 0;
}

ProcessId create_new_process() {
  return fork();
}
