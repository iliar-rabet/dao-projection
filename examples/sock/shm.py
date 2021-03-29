import sysv_ipc
import time

# Create shared memory object
memory = sysv_ipc.SharedMemory(123456)

# Read value from shared memory
memory_value = memory.read()

# Find the 'end' of the string and strip
#i = memory_value.find('\0')
#if i != -1:
#    memory_value = memory_value[:i]

while True:
    time.sleep(0.1)
    line= memory.read()
    print(line)
    memory.write("*")
    #if(line!="*"):
    #    print(line)
    line=str(memory.read())
    print(line[0])
    print(line[1])
    print(line[2])
