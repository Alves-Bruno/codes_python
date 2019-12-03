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

num_tasks = int(sys.argv[2])
# tasks = [0,0,0,0,0,0,0,0,0,0]
tasks = [[] for i in range(num_tasks)]

# print_first_csv_line(len(tasks))

sended_to = {}
received = {}

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
            print('PUT')
            print(splitted_line[2])
            line_pieces = splitted_line[2].split(' ')
            file_id = line_pieces[9]
            node_id = line_pieces[5]
            print(float(file_id) / 1000000)
            print(node_id)

            node_id_str = str(float(file_id) / 1000000)

            if(splitted_line[2].find('-nt/') != -1):
                if not (sended_to.has_key(node_id + '_nt')):
                    sended_to[node_id + '_nt'] = time_ms
            else:
                   sended_to[node_id + '_' + node_id_str] = time_ms


        
        elif(splitted_line[2].find('received') != -1):
            print('RECEIVED')
            line_pieces = splitted_line[2].split(' ')
            file_id = line_pieces[6]
            node_id = line_pieces[3]
            print(file_id)
            print(node_id)

            # received[node_id] = time_ms

            
            if(splitted_line[2].find('1348.951282') != -1):
                received[node_id + '_nt'] = time_ms
            else:
                received[node_id + file_id] = time_ms

print(sended_to)
print(received)


# Declaring a figure "gnt" 
fig, gnt = plt.subplots() 

# Setting graph attribute 
gnt.grid(True) 


count = 0
put_and_receive = {}

for putted_file in sended_to:
    print(putted_file)
    if received.has_key(putted_file):
        print(sended_to[putted_file])
        print(received[putted_file])

        new_key = str(putted_file)
        node_id = new_key.split('_')[0]
        print('key: ' + node_id)

        if not (put_and_receive.has_key(node_id)):
            put_and_receive[node_id] = count
            count = count + 1
        # put_and_receive[new_key] = count
        # gnt.broken_barh([(sended_to[putted_file],received[putted_file] - sended_to[putted_file]], ((count+1) * 10, 10), facecolors= 'orange')
        gnt.broken_barh([(sended_to[putted_file], received[putted_file] - sended_to[putted_file])],
                 ((put_and_receive[node_id] +1) * 10, 10))


print(count)
print(len(put_and_receive))


yticks_names = ['id' for i in range(len(put_and_receive))]
for node_id in put_and_receive:
    print(node_id)
    print(put_and_receive[node_id])
    yticks_names[put_and_receive[node_id]] = node_id

# Setting ticks on y-axis 
gnt.set_yticks([i+5 for i in range(10, 10 * (len(put_and_receive) + 1), 10)])
# gnt.set_yticks([5,15,25,35,45]) 

# Labelling tickes of y-axis 
gnt.set_yticklabels(yticks_names) 

plt.show()
