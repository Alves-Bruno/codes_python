import os 
import sys

def read_total_time(file_name):
    
    file = open(file_name, "r")

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
            
            file.close()

            # return ((int(time_ms) / 10) *  10) + 10
            if(len(sys.argv) == 3):
                return int(sys.argv[2])
            else:
                return ((int(time_ms) / 10) *  10) + 10


def read_total_time_hecil(file_name):
    
    file = open(file_name, "r")

    first = True
    first_time_s = 0.0000000
    first_time_usec = 0.0000000

    all_lines = file.read().splitlines()
    only_2_lines = []
    only_2_lines.append(all_lines[0])

    for line in all_lines:
        if line.find('Task 10 state change: RETRIEVED (4) to DONE (5)') != -1:
            only_2_lines.append(line)
            # print(line)

    
    # only_2_lines.append(all_lines[-1])

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
            return ((int(time_ms) / 10) *  10) + 20

            file.close()

names_blast = ['blast_normal_11W', 'blast_normal_2W', 'blast_bruno_11W', 'blast_bruno_2W', 'blast_bruno_11W_clean_cache', 'blast_bruno_2W_clean_cache']
names_hecil = ['hecil_normal_11W', 'hecil_normal_2W', 'hecil_bruno_11W', 'hecil_bruno_2W', 'hecil_bruno_11W_clean_cache', 'hecil_bruno_2W_clean_cache']

if sys.argv[1] == 'blast':
    for i in range(len(names_blast)):

        tasks = 20
        if names_blast[i] == 'blast_bruno_11W_clean_cache':
            tasks = 100
        
        file_name = 'LAST_exec/' + names_blast[i] + '_0/out.log'
        time = read_total_time(file_name)
        out1 = 'gantt_acompanhado_' + names_blast[i] + '.png'

        if(len(sys.argv) == 3):
            out1 = 'gantt_' + sys.argv[2] + '_' + names_blast[i] + '.png'

        command1 = 'python search_for_task.py ' + file_name + ' ' + str(tasks) + ' ' + out1 + ' 0-20 0-' + str(time)

        command2 = ''
        out2 = 'connected_' + names_blast[i] + '.png'
        if i % 2 == 0:
            command2 = 'python connected_nodes.py ' + file_name +' ' + str(time) + ' 12 ' + out2
        else:
            command2 = 'python connected_nodes.py ' + file_name +' '+ str(time) +' 3 ' + out2

        # print(read_total_time(file_name))
        # os.system(command)
        # print(command1)
        # os.system(command1)
        # print(command2)
        # os.system(command2)

        latex_show_fig = '\\begin{figure}[ht]\n	\caption{' + names_blast[i].replace('_', ' ') + '}\n	\label{fig:' + out1.replace('.png', '') +'}\n	\centering\n\n    \includegraphics[scale=0.5]{capitulos/images/' + out1 +'}\n    \includegraphics[scale=0.5]{capitulos/images/' + out2+ '}\n\n\end{figure}'
        print(latex_show_fig)
        print('')
        print('')

else:
    for i in range(len(names_hecil)):
        tasks = 112

        file_name = 'LAST_exec/' + names_hecil[i] + '_0/out.log'
        time = read_total_time_hecil(file_name)
        out1 = 'gantt_acompanhado_' + names_hecil[i] + '.png'
        command1 = 'python search_for_task.py ' + file_name + ' ' + str(tasks) + ' ' + out1 + ' 0-10 90-' + str(time)

        command2 = ''
        out2 = 'connected_' + names_hecil[i] + '.png'
        if i % 2 == 0:
            command2 = 'python connected_nodes.py ' + file_name +' ' + str(time) + ' 12 ' + out2
        else:
            command2 = 'python connected_nodes.py ' + file_name +' '+ str(time) +' 3 ' + out2

        # print(read_total_time(file_name))
        # os.system(command)
        # print(command1)
        # os.system(command1)
        # print(command2)
        # os.system(command2)

        latex_show_fig = '\\begin{figure}[ht]\n	\caption{' + names_hecil[i].replace('_', ' ') + '}\n	\label{fig:' + out1.replace('.png', '') +'}\n	\centering\n\n    \includegraphics[scale=0.5]{capitulos/images/' + out1 +'}\n    \includegraphics[scale=0.5]{capitulos/images/' + out2+ '}\n\n\end{figure}'
        print(latex_show_fig)
        print('')
        print('')