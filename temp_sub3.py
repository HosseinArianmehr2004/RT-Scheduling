#!/usr/bin/env python3
# ------------------------------------------
# RM_scheduling.py: Rate Monotonic Scheduler
# Author: Ragesh RAMACHANDRAN
# ------------------------------------------
import json
import copy
from sys import *
from math import gcd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from collections import defaultdict


T = []
C = []
U = []

# For gantt chart
y_axis = []
from_x = []
to_x = []


class Sub_3:
    def __init__(self):
        self.n = None
        self.hp = None
        self.tasks = dict()
        self.dList = None
        self.metrics = defaultdict(dict)
        self.realTime_task = dict()

    def read_data(self):
        """
        Reading the details of the tasks to be scheduled from the user as
        Number of tasks n:
        Period of task P:
        Worst case excecution time WCET:
        """

        self.dList = {}

        n = int(input("Enter number of Tasks:"))
        self.n = n

        # Storing data in a dictionary
        for i in range(n):
            self.dList["TASK_%d" % i] = {"start": [], "finish": []}
        self.dList["TASK_IDLE"] = {"start": [], "finish": []}

        for i in range(n):
            self.tasks[i] = {}
            print("Enter Period of task T", i, ":")
            p = input()
            self.tasks[i]["Period"] = int(p)
            print("Enter the WCET of task C", i, ":")
            w = input()
            self.tasks[i]["WCET"] = int(w)

        # Writing the dictionary into a JSON file
        with open("self.tasks.json", "w") as outfile:
            json.dump(self.tasks, outfile, indent=4)

    def hyperperiod(self):
        """
        Calculates the hyper period of the tasks to be scheduled
        """
        temp = []
        n = self.n
        for i in range(n):
            temp.append(self.tasks[i]["Period"])
        HP = temp[0]
        for i in temp[1:]:
            HP = HP * i // gcd(HP, i)
        print("Hyperperiod:", HP)
        return HP

    def schedulablity(self):
        """
        Calculates the utilization factor of the tasks to be scheduled
        and then checks for the schedulablity and then returns true is
        schedulable else false.
        """
        n = self.n
        for i in range(n):
            T.append(int(self.tasks[i]["Period"]))
            C.append(int(self.tasks[i]["WCET"]))
            u = int(C[i]) / int(T[i])
            U.append(u)

        U_factor = sum(U)
        if U_factor <= 1:
            print("Utilization factor: ", U_factor, "underloaded tasks")

            sched_util = n * (2 ** (1 / n) - 1)
            print("Checking condition: ", sched_util)

            count = 0
            T.sort()
            for i in range(len(T)):
                if T[i] % T[0] == 0:
                    count = count + 1

            # Checking the schedulablity condition
            if U_factor <= sched_util or count == len(T):
                print("Tasks are schedulable by Rate Monotonic Scheduling!")
                return True
            else:
                print("Tasks are not schedulable by Rate Monotonic Scheduling!")
                return False
        print("Overloaded tasks!")
        print("Utilization factor > 1")
        return False

    def estimatePriority(self, realTime_task):
        """
        Estimates the priority of tasks at each real time period during scheduling
        """
        tempPeriod = self.hp
        P = -1  # Returns -1 for idle tasks
        for i in realTime_task.keys():
            if realTime_task[i]["WCET"] != 0:
                if (
                    tempPeriod > realTime_task[i]["Period"]
                    or tempPeriod > self.tasks[i]["Period"]
                ):
                    tempPeriod = self.tasks[i][
                        "Period"
                    ]  # Checks the priority of each task based on period
                    P = i
        return P

    def simulation(self, hp):
        """
        The real time schedulng based on Rate Monotonic scheduling is simulated here.
        """

        # Real time scheduling are carried out in realTime_task
        realTime_task = self.realTime_task
        realTime_task = copy.deepcopy(self.tasks)
        # validation of schedulablity neessary condition
        for i in realTime_task.keys():
            realTime_task[i]["DCT"] = realTime_task[i]["WCET"]
            if realTime_task[i]["WCET"] > realTime_task[i]["Period"]:
                print("The task can not be completed in the specified time ! ", i)

        # main loop for simulator
        for t in range(hp):
            # Determine the priority of the given tasks
            priority = self.estimatePriority(realTime_task)

            if priority != -1:  # processor is not idle
                print("t{}-->t{} :TASK{}".format(t, t + 1, priority))
                # Update WCET after each clock cycle
                realTime_task[priority]["WCET"] -= 1
                # For the calculation of the metrics
                self.dList["TASK_%d" % priority]["start"].append(t)
                self.dList["TASK_%d" % priority]["finish"].append(t + 1)
                # For plotting the results
                y_axis.append("TASK%d" % priority)
                from_x.append(t)
                to_x.append(t + 1)

            else:  # processor is idle
                print("t{}-->t{} :IDLE".format(t, t + 1))
                # For the calculation of the metrics
                self.dList["TASK_IDLE"]["start"].append(t)
                self.dList["TASK_IDLE"]["finish"].append(t + 1)
                # For plotting the results
                y_axis.append("IDLE")
                from_x.append(t)
                to_x.append(t + 1)

            # Update Period after each clock cycle
            for i in realTime_task.keys():
                realTime_task[i]["Period"] -= 1
                if realTime_task[i]["Period"] == 0:
                    realTime_task[i] = copy.deepcopy(self.tasks[i])

            with open("RM_sched.json", "w") as outfile2:
                json.dump(self.dList, outfile2, indent=4)

    def drawGantt(self):
        """
        The scheduled results are displayed in the form of a
        gantt chart for the user to get better understanding
        """
        n = self.n
        colors = ["red", "green", "blue", "orange", "yellow"]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # the data is plotted from_x to to_x along y_axis
        ax = plt.hlines(y_axis, from_x, to_x, linewidth=20, color=colors[n - 1])
        plt.title("Rate Monotonic scheduling")
        plt.grid(True)
        plt.xlabel("Real-Time clock")
        plt.ylabel("HIGH------------------Priority--------------------->LOW")
        plt.xticks(np.arange(min(from_x), max(to_x) + 1, 1.0))
        plt.show()

    def showMetrics(self):
        """
        Displays the resultant metrics after scheduling such as
        average response time, the average waiting time and the
        time of first deadline miss
        """
        N = []
        startTime = []
        releaseTime = []
        finishTime = []
        avg_respTime = []
        avg_waitTime = []

        # Calculation of number of releases and release time
        for i in self.tasks.keys():
            release = int(self.hp) / int(self.tasks[i]["Period"])
            N.append(release)
            temp = []
            for j in range(int(N[i])):
                temp.append(j * int(self.tasks[i]["Period"]))
            # temp.append(self.hp)
            releaseTime.append(temp)

        # Calculation of start time of each task
        for j, i in enumerate(self.tasks.keys()):
            start_array, end_array = self.filter_out(
                self.dList["TASK_%d" % i]["start"],
                self.dList["TASK_%d" % i]["finish"],
                N[j],
            )
            startTime.append(start_array)
            finishTime.append(end_array)

        # Calculation of average waiting time and average response time of tasks
        for i in self.tasks.keys():
            avg_waitTime.append(
                st.mean([a_i - b_i for a_i, b_i in zip(startTime[i], releaseTime[i])])
            )
            avg_respTime.append(
                st.mean([a_i - b_i for a_i, b_i in zip(finishTime[i], releaseTime[i])])
            )

        # Printing the resultant metrics
        for i in self.tasks.keys():
            self.metrics[i]["Releases"] = N[i]
            self.metrics[i]["Period"] = self.tasks[i]["Period"]
            self.metrics[i]["WCET"] = self.tasks[i]["WCET"]
            self.metrics[i]["AvgRespTime"] = avg_respTime[i]
            self.metrics[i]["AvgWaitTime"] = avg_waitTime[i]

            print("Number of releases of task %d =" % i, int(N[i]))
            print("Release time of task%d = " % i, releaseTime[i])
            print("start time of task %d = " % i, startTime[i])
            print("finish time of task %d = " % i, finishTime[i])
            print("Average Response time of task %d = " % i, avg_respTime[i])
            print("Average Waiting time of task %d = " % i, avg_waitTime[i])
            print()

        # Storing results into a JSON file
        with open("Metrics.json", "w") as f:
            json.dump(self.metrics, f, indent=4)
        print("Scheduling of %d tasks completed succesfully...." % self.n)

    def filter_out(self, start_array, finish_array, release_time):
        """A filtering function created to create the required data struture from the simulation results"""
        new_start = []
        new_finish = []
        beg_time = min(start_array)
        diff = int(self.hp / release_time)
        # Calculation of finish time and start time from simulation results
        if release_time > 1:
            new_start.append(beg_time)
            prev = beg_time
            for i in range(int(release_time - 1)):
                beg_time = beg_time + diff
                new_start.append(beg_time)
                count = start_array.index(prev)
                for i in range(
                    start_array.index(prev), start_array.index(beg_time) - 1
                ):
                    count += 1
                new_finish.append(finish_array[count])
                prev = beg_time
            new_finish.append(max(finish_array))

        else:
            end_time = max(finish_array)
            new_start.append(beg_time)
            new_finish.append(int(end_time))
        return new_start, new_finish

    def start(self):
        print("RATE MONOTONIC SCHEDULER\n")
        self.read_data()

        sched_res = self.schedulablity()
        if sched_res == True:
            self.hp = self.hyperperiod()
            self.simulation(self.hp)
            self.showMetrics()
            self.drawGantt()
        else:
            self.read_data()
            sched_res = self.schedulablity()


sub = Sub_3()
sub.start()
