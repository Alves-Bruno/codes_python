#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys 
# Importing the matplotlb.pyplot 
import matplotlib.pyplot as plt 
import os

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



avg_times = []

folders = []
folders = os.listdir(sys.argv[1])
# print(folders)

filtered_folders = []

for folder_name in folders:
    # print(folder_name[:-1])
    if folder_name[:-1] not in filtered_folders:
        if(folder_name.find(sys.argv[2]) != -1):
            filtered_folders.append(folder_name[:-1])

print(filtered_folders)

for folder_name in filtered_folders:
    
    TOTAL_TIME = 0.0000000

    for i in range(10):

        file_name = sys.argv[1] + '/' + folder_name + str(i) + '/out.log'
        # print(file_name)
        file = open(file_name, "r")
        # line = f.readline()
        # print(line) 

        first = True
        first_time_s = 0.0000000
        first_time_usec = 0.0000000

        all_lines = file.read().splitlines()
        only_2_lines = []
        only_2_lines.append(all_lines[0])
        only_2_lines.append(all_lines[-1])

        for line in only_2_lines:
            splitted_line = line.split('#|')
            if(len(splitted_line) >= 3):
                times = splitted_line[1].split('|')[0].split('.')
                time_sec = float(times[0])
                time_usec = float(times[1])

                if first:
                    first_time_s = time_sec
                    first_time_usec = time_usec
                    first = False
                    continue

                diff_sec = time_sec - first_time_s
                diff_usec = time_usec - first_time_usec
                time_ms = diff_sec * 1000 + diff_usec/1000000

                time_ms = time_ms / 1000

                # print(time_ms)
                TOTAL_TIME = TOTAL_TIME + time_ms

                file.close()

    avg_times.append((folder_name[:-1], TOTAL_TIME/10))
    # print(TOTAL_TIME/10)

def sort_by_time(elemento):
    return elemento[1]

print(avg_times)
avg_times.sort(key=sort_by_time)
# print('')

x_names = [i[0] for i in avg_times]

for i in range(len(x_names)):
    x_names[i] = x_names[i].replace('clean_cache', 'cache_vazia')
    x_names[i] = x_names[i].replace('blast', '')
    x_names[i] = x_names[i].replace('hecil', '')
    x_names[i] = x_names[i].replace('_', '\n')
    # x_names[i] = x_names[i].replace('', '')
    x_names[i] = x_names[i].replace('normal', 'cctools')
    x_names[i] = x_names[i].replace('bruno', 'modificado')
    x_names[i] = x_names[i].replace('W', '')
    # x_names[i] = x_names[i].replace('blast', '')



y_values = [i[1] for i in avg_times]

x_ticks = [i for i in range(len(avg_times))]

plt.bar(x_ticks, y_values, align='center', alpha=0.5)
plt.xticks(x_ticks, x_names)
plt.ylabel('Tempo (segundos)')
plt.xlabel(u'Cenário Testado')
# plt.xticks(rotation=75)
# plt.title('Tem')

plt.tight_layout()

# Setting graph attribute 
plt.grid(True) 

plt.savefig(sys.argv[2] + '.png', format='png', dpi=500)
# plt.show()

