import socket
from test import *
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 5000))

# left-down
d1 = Disk("B", BLACK, 1, 1, 5)
d2 = Disk("A", RED, 1, 2, 5)
# right-down
d3 = Disk("B", RED, 2, 3, 3)
d4 = Disk("&", BLACK, 2, 4, 3)
# left-up
d5 = Disk("R", BLACK, 3, 5, 1)
d6 = Disk("B", RED, 3, 6, 1)
# right-up
d7 = Disk("T", BLUE, 4, 7, 7)
d8 = Disk("H", BLUE, 4 ,8, 7)


disk_info = [0, d1, d2, d3, d4, d5, d6, d7, d8]
disk_mother = DiskMother()
target_seq = [Disk("A", RED), Disk("B", RED), Disk("B", RED), EMPTY_DISK, Disk("B", BLACK), Disk("&", BLACK), Disk("R", BLACK), EMPTY_DISK]

p = Path()
generate_path(disk_info, disk_mother, p, target_seq, 0)
best_path, least_rotation = evaluation(PATHS, DEGREES) # robot faster? disk faster?
p = best_path
p.init()




while True:
    data1 = p.deque_one_instruction()
    if data1 == END_SIGN:
        p.end()
        break
    sock.send(data1.encode())
    data2 = sock.recv(1024)
    if not data2:
        break
    print(data2.decode('utf-8') + ": " + data1)

time.sleep(5)
sock.close()
