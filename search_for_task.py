#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys 
# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatch
# import matplotlib.pyplot as plt


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
        
        if(splitted_line[2].find('Task') != -1):
            if(splitted_line[2].find('UNKNOWN (0) to WAITING (1)') != -1):
                task_id = get_task_id(splitted_line[2])
                print(task_id)
                tasks[task_id].append((time_ms,1))
                # print_csv_line(time_ms, tasks)

            elif(splitted_line[2].find('WAITING (1) to RUNNING (2)') != -1):
                task_id = get_task_id(splitted_line[2])
                tasks[task_id].append((time_ms, 2))

            elif(splitted_line[2].find('RUNNING (2) to WAITING_RETRIEVAL (3)') != -1):
                task_id = get_task_id(splitted_line[2])
                tasks[task_id].append((time_ms, 3))

            elif(splitted_line[2].find('WAITING_RETRIEVAL (3) to RETRIEVED (4)') != -1):
                task_id = get_task_id(splitted_line[2])
                tasks[task_id].append((time_ms, 4))
                

            elif(splitted_line[2].find('RETRIEVED (4) to DONE (5)') != -1):
                task_id = get_task_id(splitted_line[2])
                tasks[task_id].append((time_ms, 5))



# Declaring a figure "gnt" 
fig, gnt = plt.subplots() 

# Setting Y-axis limits 
# gnt.set_ylim(0, 50) 

# Setting X-axis limits 
if len(sys.argv) > 5:
    # print(sys.argv[5])
    x_0 = int(sys.argv[5].split('-')[0])
    x_final = int(sys.argv[5].split('-')[1])
    gnt.set_xlim(x_0, x_final) 

    # if x_final % 100 == 0:
    #     # Setting ticks on y-axis 
    #     gnt.set_xticks([i for i in range(x_0, x_final + 100, 100)]) 
    #     # Labelling tickes of y-axis 
    #     gnt.set_xticklabels([str(i) for i in range(x_0, x_final + 100, 100)]) 
    # elif x_final % 50 == 0:
    #     # Setting ticks on y-axis 
    #     gnt.set_xticks([i for i in range(x_0, x_final + 50, 50)]) 
    #     # Labelling tickes of y-axis 
    #     gnt.set_xticklabels([str(i) for i in range(x_0, x_final + 50, 50)]) 
    # elif x_final % 20 == 0:
    #     # Setting ticks on y-axis 
    #     gnt.set_xticks([i for i in range(x_0, x_final + 20, 20)]) 
    #     # Labelling tickes of y-axis 
    #     gnt.set_xticklabels([str(i) for i in range(x_0, x_final + 20, 20)]) 
    # elif x_final % 10 == 0:
    #     # Setting ticks on y-axis 
    #     gnt.set_xticks([i for i in range(x_0, x_final + 10, 10)]) 
    #     # Labelling tickes of y-axis 
    #     gnt.set_xticklabels([str(i) for i in range(x_0, x_final + 10, 10)]) 



# Setting labels for x-axis and y-axis 
gnt.set_xlabel('Tempo (segundos)') 
gnt.set_ylabel(u'Número Identificador da Tarefa') 



# Setting ticks on y-axis 
gnt.set_yticks([i+5 for i in range(10, num_tasks * 10 + 50, 10)]) 
# Labelling tickes of y-axis 
gnt.set_yticklabels([str(i) for i in range(1,num_tasks+1)]) 

# Setting graph attribute 
gnt.grid(True) 

def sort_by_time(reg):
    return reg[0]


bar_colors = ["yellow", "red", "green", "blue"]
# yellow_patch = mpatches.Patch(color='yellow', label='Tarefa em Espera.')
# red_patch = mpatches.Patch(color='red', label='Tarefa executando.')
# green_patch = mpatches.Patch(color='green', label='Tarefa esperando para envio dos resultados.')

start = int(sys.argv[4].split('-')[0])
end = int(sys.argv[4].split('-')[1])

for i in range(start, end):
    
    # task_reg.sort(key=sort_by_time)
    # print(task_reg)
    # # for time_taken in tasks[i]:
    #     # print(time_taken[1])

    #print(tasks[i])

    for registro in range(len(tasks[i])):
        if tasks[i][registro][1] <= 4:
            #print(i)
            #print(tasks[i][registro])
            gnt.broken_barh([(tasks[i][registro][0], tasks[i][registro+1][0] - tasks[i][registro][0])], ((i+1) * 10, 10), label="a", facecolors =(bar_colors[tasks[i][registro][1] - 1]))
        # if tasks[i][registro][1] == 2:
            # gnt.broken_barh([(tasks[i][registro][0], tasks[i][registro+1][0] - tasks[i][registro][0])], (i+1 * 10, 1), facecolors =('blue'))

    # print('')

# plt.legend(handles=[red_patch, yellow_patch, green_patch])

fakeyellowbar = mpatch.Rectangle((0, 0), 1, 1, fc="y")
fakeredbar = mpatch.Rectangle((0, 0), 1, 1, fc="r")
fakegreenbar = mpatch.Rectangle((0, 0), 1, 1, fc="g")
gnt.legend([fakeyellowbar, fakeredbar, fakegreenbar], ['Em espera', 'Executando', 'Envio dos resultados'],loc='upper center', bbox_to_anchor=(0.5, 1.11),
          fancybox=True, shadow=True, ncol=3)

# gnt.legend([fakeyellowbar, fakeredbar], ['Em espera', 'Executando'],loc='upper center', bbox_to_anchor=(0.5, 1.11),
        #   fancybox=True, shadow=True, ncol=2)


fig.subplots_adjust(bottom=0.13) # or whatever


# plt.show()
plt.savefig(sys.argv[3], format='png', dpi=100)