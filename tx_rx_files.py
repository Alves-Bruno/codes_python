import sys 
# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 

def get_task_id(line_str):
    task_id = line_str.replace('Task', '@')
    task_id = task_id.replace('state', '@')
    task_id = task_id.split("@")[1]
    task_id_int = int(task_id)
    return task_id_int - 1

# def print_csv_line(time_ms, tasks):
#     print(str(time_ms), end='')
#     for i in tasks:
#         print(', ' + str(i), end = '')
#     print('')    

# def print_first_csv_line(tasks_num):
#     print('time', end='')
#     for i in range(0, tasks_num):
#         print(',task' + str(i), end='')
#     print('')


file = open(sys.argv[1], "r")
# line = f.readline()
# print(line) 

first = True
first_time_s = 0.0000000
first_time_usec = 0.0000000

# num_tasks = int(sys.argv[2])
# tasks = [0,0,0,0,0,0,0,0,0,0]
# tasks = [[] for i in range(num_tasks)]

# print_first_csv_line(len(tasks))

TX_total = 0.00000
RX_total = 0.00000

for line in file:
    splitted_line = line.split('#|')
    if(len(splitted_line) >= 3):
        times = splitted_line[1].split('|')[0].split('.')
        time_sec = float(times[0])
        time_usec = float(times[1])

        if first:
            first_time_s = time_sec
            first_time_usec = time_usec
            first = False

        diff_sec = time_sec - first_time_s
        diff_usec = time_usec - first_time_usec
        time_ms = diff_sec * 1000 + diff_usec/1000000
        
        if(splitted_line[2].find('put') != -1):
            # print('PUT')
            # print(splitted_line[2])
            line_pieces = splitted_line[2].split(' ')
            # file_id = line_pieces[9]
            # node_id = line_pieces[5]
            # print(float(line_pieces[9]) / 1024)
            TX_total = TX_total + (float(line_pieces[9])) 


        
        elif(splitted_line[2].find('Receiving') != -1):
            # print('RECEIVED')
            # print(splitted_line[2])
            line_pieces = splitted_line[2].split(' ')
            # file_id = line_pieces[6]
            # node_id = line_pieces[3]
            # print(float(line_pieces[7]) / 1024)
            RX_total = RX_total + (float(line_pieces[7]))
            

print('TX: ' + str(TX_total/ (1024 * 1024) ) + " MB")
print('RX: ' + str(RX_total/ (1024 * 1024)) + " KB")