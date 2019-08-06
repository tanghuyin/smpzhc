import copy
import numpy as np

FINISH_SIGN = "finished one instruction"
END_SIGN = "f"
ROTATE_45 = "45"
ROTATE_90 = "90"
ROTATE_135 = "135"
ROTATE_180 = "180"
ROTATE_45_INV = "45_inv"
ROTATE_90_INV = "90_inv"
ROTATE_135_INV = "135_inv"
ROTATE_180_INV = "180_inv"
DISK_1 = "01"
DISK_2 = "02"
DISK_3 = "03"
DISK_4 = "04"
DISK_5 = "05"
DISK_6 = "06"
DISK_7 = "07"
DISK_8 = "08"
RED = "red"
BLACK = "black"
BLUE = "blue"
PATHS = []
DEGREES = []



class Disk:
    def __init__(self, letter, color=None, pos=None, no=None, put_in=None):
        self.letter = letter
        self.color = color
        self.pos = pos
        self.no = no
        self.put_in = put_in

class Node:
    def __init__(self, data, pnext=None, pprev=None):
        self.data = data
        self.next = pnext
        self.prev = pprev

class Path:
    def __init__(self):
        self.head = None
        self.tail = None
        self.now = None
        self.length = 0
    
    def append(self, inst):
        if not self.head and not self.tail:
            self.head = Node(inst, self.tail)
            self.tail = self.head
            self.tail.prev = self.head
            self.length += 1
        else:
            a = Node(inst, None, self.tail)
            self.tail.next = a
            self.tail = self.tail.next
            self.length += 1
    def pop(self):
        self.length -= 1
        self.tail = self.tail.prev
        if self.length == 0:
            self.head = None
            self.tail = None
            self.now = None
            self.length = 0

        return
    
    def getLength(self):
        return self.length


    def init(self):
        print("There " + str(self.length) + " instrutions in all.")
        print("Now start the first instructions.")


    def print(self):
        a = self.head
        while a:
            print(a.data, end=' ')
            a = a.next

    def deque_one_instruction(self):
        if not self.now:
            self.now = self.head
        else:
            self.now = self.now.next
        
        if self.now:
            return self.now.data
        else:
            return "f"
    
    def end(self):
        print("All instructions have been executed.")


EMPTY_DISK = Disk("?")
class DiskMother:
    def __init__(self):
        self.list = [EMPTY_DISK] * 8

    def isEmpty(self):
        for i in range(8):
            if self.list[i] != EMPTY_DISK:
                return False
        return True

    def insert_disk(self, disk):
        self.list[disk.put_in] = disk
        return eval("DISK_" + str(disk.no))

    def print_disk_mother(self):
        print("    " + self.list[0].letter)
        print("  " + self.list[7].letter, "  " + self.list[1].letter)
        print(self.list[6].letter, "      " + self.list[2].letter)
        print("  " + self.list[5].letter, "  " + self.list[3].letter)
        print("    " + self.list[4].letter)

    def mother_rotate(self, dir):
        if dir == 0:
            return
        if dir % 45 != 0:
            print("Wrong input of degree")
            return
        rr = int(dir / 45)
        if rr > 0:
            for i in range(rr):
                t = self.list.pop()
                self.list.insert(0, t)
            return eval("ROTATE_" + str(dir))
        else:
            for i in range(-rr):
                t = self.list[0]
                self.list = self.list[1:]
                self.list.append(t)
            return eval("ROTATE_" + str(-dir) + "_INV")
    def isFinish(self, t1, t2, target_seq):
        for i in range(8):
            if isFinish(t1, t2):
                return True   
            rotate(target_seq)
        return False
    def remove_disk(self, disk):
        self.list[disk.put_in] = EMPTY_DISK

            
        
            

def judge_avail(disk):
    if not disk:
        return False
    if disk.letter in ["B", "A", "R", "&"]:
        if disk.color in [RED, BLACK]:
            return True
    return False

def rotate(seq):
    a = seq.pop()
    seq = seq.insert(0, a)

def isEqual(t1, t2):
    if len(t1) != len(t2):
        print("Lengths are not the same")
    for i in range(len(t1)):
        if t2[i].letter == '?':
            continue
        if t1[i].letter != t2[i].letter:
            return False
        if t1[i].color != t2[i].color:          
            return False
    return True

def isFinish(t1, t2):
    if len(t1) != len(t2):
        print("Lengths are not the same")
    for i in range(len(t1)):
        if t1[i].letter != t2[i].letter:
            return False
        if t1[i].color != t2[i].color:          
            return False
    return True

def findLeastRotate(target_seq, disk, disk_mother):
    for i in range(len(target_seq)):
        if target_seq[i].letter == disk.letter and target_seq[i].color == disk.color:
            # 3, 4 should be 1
            # 0, 7 should be -1
            d = (disk.put_in - i) * 45 if abs(i - disk.put_in) <= 4 else ((disk.put_in - i) - 8) * 45 if disk.put_in - i > 0 else ((disk.put_in - i) + 8) * 45
            disk_mother.mother_rotate(d)
            if disk_mother.list[disk.put_in] == EMPTY_DISK:
                disk_mother.mother_rotate(-d)
                return d
            else:
                disk_mother.mother_rotate(-d)

    print("No Possible Rotate??")
    return -1
# ABB B&R
def generate_path(disk_info, disk_mother, path, target_seq, all_degree):
    # Use recursive, find the path which make the turning time of disk mother least
    '''
    First, the robot need to find an initial point, since the robot near pos 3, 4 at default condition, we choose possible point from no 5, 6, 7, 8
    No disk on disk mother at the beginning, each is possible, for most concern. !! More complex situation may need to be handled
    '''
    # judge if left-up has disk
    
    
    if disk_mother.isFinish(target_seq, disk_mother.list, target_seq):
        PATHS.append(copy.deepcopy(path))
        DEGREES.append(all_degree)
        return
    '''
    # This is for debug

    for i in range(8):
        print(target_seq[i].letter, end = ' ')
    print()
    '''
    if disk_mother.isEmpty():
        for no in [5, 6, 7, 8]:
            if judge_avail(disk_info[no]):
                tmp_1 = copy.deepcopy(target_seq)
                instruction = disk_mother.insert_disk(disk_info[no])
                path.append(instruction)
                tmp_2 = copy.deepcopy(disk_info[no])
                disk_info[no] = None
                while not isEqual(target_seq, disk_mother.list):
                    rotate(target_seq)
                generate_path(disk_info, disk_mother, path, target_seq, all_degree)
                # re-start
                path.pop()
                disk_mother.remove_disk(tmp_2)
                disk_info[no] = tmp_2
                target_seq = tmp_1
    else:
        for no in [5, 6, 7, 8, 4, 3, 2, 1]: # As long as the disk is available, it need to be put in the disk mother
            if judge_avail(disk_info[no]):
                tmp_1 = copy.deepcopy(target_seq)
                degree = findLeastRotate(target_seq, disk_info[no], disk_mother)
                if degree != 0:
                    all_degree += abs(degree)
                    instruction = disk_mother.mother_rotate(degree)
                    path.append(instruction)
                instruction = disk_mother.insert_disk(disk_info[no])
                path.append(instruction)
                rotate_time = 0
                while not isEqual(target_seq, disk_mother.list):
                    rotate(target_seq)
                    rotate_time += 1
                    if rotate_time == 8:
                        target_seq = list(reversed(target_seq))
                        rotate_time = 0
                tmp_2 = copy.deepcopy(disk_info[no])
                disk_info[no] = None     
                generate_path(disk_info, disk_mother, path, target_seq, all_degree)
                # re-start, Strange
                path.pop()
                disk_mother.remove_disk(tmp_2)
                if degree != 0:
                    all_degree -= abs(degree)
                    disk_mother.mother_rotate(-degree)
                    path.pop()
                target_seq = tmp_1
                disk_info[no] = tmp_2
                # generate_path(copy.deepcopy(disk_info), copy.deepcopy(disk_mother), copy.deepcopy(path), copy.deepcopy(target_seq))
                


def get_move(path):
    last = -1
    move_time = 0
    for i in range(path.getLength()):
        a = path.deque_one_instruction()
        if a[0] == '0':
            no = int(a[1]) - 1
            if int(no / 2) != last:
                move_time += 1
                last = int(no / 2)
    return move_time

def evaluation(paths, degrees):
    min_ind = degrees.index(min(degrees))
    moves = []
    deg_sort = np.argsort(degrees)
    for index in deg_sort: 
        step = get_move(copy.deepcopy(PATHS[index]))
        if step == 4:
            return paths[index], degrees[min_ind]



'''
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
best_path, least_rotation = evaluation(PATHS, DEGREES)


'''