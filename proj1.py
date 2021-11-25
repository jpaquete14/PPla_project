def parseInput():
    lines = sys.stdin.readlines()

    lst_aux = lines[0].strip('\n').split(" ")

    n_jobs = int(lst_aux[0])
    n_machines = int(lst_aux[1])

    tasks = []

    for i in range(1, n_jobs + 1):
        lst_aux2 = []
        lst_aux1 = lines[i].strip('\r\n').split(" ")
        k = int(lst_aux1[0])
        lst_aux2.append(k)

        for j in range(1, k + 1):
            lst_aux2.append(lst_aux1[j].split(":"))

        tasks.append(lst_aux2)


    return [n_jobs, n_machines, tasks]


def print_info(info):
    print("n_jobs - " + str(info[0]) + "; n_machines - " + str(info[1]))
    print("info:")

    for i in range(info[0]):
        print(info[2][i])


def create_data(info):
    tasks = []
    strg = ""

    strg += "(define (problem proj1)\n\n"
    strg += "\t(:domain tasksworld)\n\n"
    strg += "\t(:objects\n\t\t"

    for i in range(1, info[1] + 1):
        strg += "M" + str(i) + " "

    strg += "- machine\n"

    strg += "\t\tNone "

    count = 1
    for i in range(info[0]):

        d = int(info[2][i][0])
        for j in range(1, d + 1):
            tasks_aux = []

            for t in range(1, int(info[2][i][j][1]) + 1):
                strg += "T" + str(count) + "_" + str(t) + " "
                tasks_aux.append("T" + str(count) + "_" + str(t))

            count += 1

            tasks.append(tasks_aux)


    strg += " - task\n"
    strg += "\t)\n\n"

    strg += "\t(:init\n\n"

    count = 0
    for i in range(info[0]):

        t = info[2][i][0]
        for j in range(t):

            if j != 0:
                strg += "\t\t(must-be-done " + tasks[count][0] + " " + tasks[count - 1][-1] + ")\n"

            else:
                strg += "\t\t(must-be-done " + tasks[count][0] + " None)\n"

            count += 1

    strg += "\n"

    len_tasks = len(tasks)
    for i in range(len_tasks):

        len_sub_tasks = len(tasks[i])
        for j in range(len_sub_tasks - 1, 0, -1):

            if j > 0:
                strg += "\t\t(must-be-next " + tasks[i][j] + " " + tasks[i][j - 1] + ")\n"

    strg += "\n"
    for i in range(len_tasks):

        strg += "\t\t(must-be-first " + tasks[i][0] + ")\n"

    strg += "\n"
    count = 0
    for i in range(info[0]):

        len_job = info[2][i][0]
        for j in range(len_job):

            len_sub_tasks = len(tasks[count])
            strg += "\t\t(on_machine " + tasks[count][0] + " M" + info[2][i][j + 1][0] + ")\n"

            count += 1

    for i in range(info[1]):
        strg += "\n\t\t(on_machine None M" + str(i + 1) + ")"
        strg += "\n\t\t(prev_task None M" + str(i + 1) + ")"

    strg += "\n"

    for i in range(1, info[1]):
        strg += "\n\t\t(next_machine M" + str(i) + " M" + str(i + 1) + ")"

    strg += "\n\t\t(next_machine M" + str(i + 1) + " M1)"

    strg += "\n\n\t\t(prev_machine M" + str(info[1]) + ")"

    strg += "\n\t\t(None None)"
    strg += "\n\t\t(done None)\n"
    strg += "\n\t\t(= (total_cost) 0)\n"
    strg +="\t)\n\n"

    strg += "\t(:goal"
    strg += "\n\t\t(and"
	
  
    for i in range(len_tasks):

        len_sub_tasks = len(tasks[i])
        strg += "\n\t\t\t(done " + tasks[i][-1] + ")"

    strg += "\n\t\t)"
    strg += "\n\t)\n\n"

    strg += "\t(:metric minimize (total-cost))\n\n"
    strg += ")\n"


    return [strg, len_tasks]


def CSP(data):

    f = open("instance_ex.pddl", "w")
    f.write(data[0])
    f.close()

    search_method = '--search "astar(blind())"'
    if data[1] > 11:
        search_method = '--evaluator "hcea=cea()" --search "lazy_greedy([hcea], preferred=[hcea])"'

    f1 = open("output.txt", "w")

    os.system('./fast-downward.py --plan-file output.txt domain_3.pddl instance_ex.pddl ' + search_method + ' > trash.txt')
    os.system('rm trash.txt')

    f1.close()


def update_info(info, strg, time):
    n_jobs = info[0]

    count = 0
    for i in range(n_jobs):
        count += info[2][i][0]
        len_job = info[2][i][0]

        if count >= int(strg):
            ind = count - int(strg)
            info[2][i][-1 - ind][1] = time
            return



def print_output(info):

    f = open("output.txt", "r")
    lines = f.readlines()

    final_cost = (int(lines[-1].split(" ")[3]) - 1) // info[1]
    final_cost += 1
    print(final_cost)
    print(str(info[0]) + " " + str(info[1]))

    time = 0
    for i in range(len(lines) - 1):

        strg = lines[i].split(" ")[-1]
        strg_aux = strg.split("_")

        if len(strg_aux) > 1:

            if strg_aux[1][:-2] == '1':
                update_info(info, strg_aux[0][1:], time)

        if ((i % info[1]) == (info[1] - 1)):
            time += 1


    strg = ""
    for i in range(info[0]):
        strg += str(info[2][i][0])

        len_job = info[2][i][0]
        for j in range(1, len_job + 1):
            strg += " " + info[2][i][j][0] + ":" + str(info[2][i][j][1])

        strg += "\n"

    print(strg)

######################################################################

import os
import sys
import itertools
import subprocess

info = parseInput()

data = create_data(info)
CSP(data)

print_output(info)
