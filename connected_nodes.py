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

x_values = [0.000]
y_values = [0]


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

        time_ms = time_ms / 1000
        
        if(splitted_line[2].find('workers are connected') != -1):
            new_line = splitted_line[2].split(' ')
            #print(new_line[3])
            x_values.append(time_ms)
            y_values.append(int(new_line[3]))
  

x_values.append(float(sys.argv[2]))
y_values.append(y_values[-1])



nodes = int(sys.argv[3]) + 1
plt.plot(x_values, y_values, linewidth=2)
y_ticks = [i for i in range(nodes)]
y_names = [str(i) for i in range(nodes)]
plt.yticks(y_ticks, y_names)
plt.ylabel('Trabalhadores Conectados')
plt.xlabel('Tempo (segundos)')
# plt.title('')

# plt.xlim(0, int(sys.argv[2]))
plt.xlim(90, int(sys.argv[2]))


# Setting graph attribute 
plt.grid(True) 


# x_ticks = [i for i in range(0, x_values[-1], 10)]
# x_names = [str(i) for i in range(0, x_values[-1], 10)]
# plt.xticks(rotation='vertical')
# plt.show()
# plt.set_size_inches(18.5, 10.5)
plt.savefig(sys.argv[4], format='png', dpi=100)