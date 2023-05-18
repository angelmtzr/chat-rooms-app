#ifndef PROCESS_H
#define PROCESS_H

#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

typedef pid_t ProcessId;

int is_main_process(ProcessId id);

ProcessId create_new_process();

#endif //PROCESS_H
