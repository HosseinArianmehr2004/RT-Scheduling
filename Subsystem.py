# from sys import *
import heapq
from math import gcd
import matplotlib.pyplot as plt
import numpy as np
from Task import *
from Core import *


class Subsystem:
    def __init__(self, id, resources):
        self.id = id
        self.resources = resources
        self.ready_queue = []

        self.file = None
        self.time = None

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue {[task.name for task in self.waiting_queue]}\n"
        )
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}"
            status += f", remaining quantum: {core.current_task.remaining_quantum if core.current_task else '-'}\n"
            status += f"                Ready Queue: {[task.name for task in core.ready_queue]}\n"
        return status

    def allocate_resources(self, task):
        for resource, needed in task.resources_needed.items():
            if self.resources[resource].available_units < needed:
                return False
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units -= needed
        task.has_all_resources = True
        return True

    def release_resources(self, task):
        for resource, needed in task.resources_needed.items():
            self.resources[resource].available_units += needed

    def execute(self):
        pass

    def set_file(self, file):
        self.file = file

    def set_time(self, time):
        self.time = time

    # def add_task(self, task):
    #     if self.allocate_resources(task):
    #         core = self.select_core()
    #         core.assign_task(task)
    #     else:
    #         self.waiting_queue.append(task)
    #         task.state = Task_State.WAITING

    def add_task(self, task):
        pass


class Subsystem_1(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_1(i, self) for i in range(num_cores)]

    def load_balancing(self):
        # Identify underloaded and overloaded cores
        underloaded_cores = [
            core
            for core in self.cores
            if not core.ready_queue and core.current_task is None
        ]
        overloaded_cores = [core for core in self.cores if len(core.ready_queue) > 1]

        # Perform pull migration
        for underloaded_core in underloaded_cores:
            for overloaded_core in overloaded_cores:
                if overloaded_core.ready_queue:
                    # Transfer a task from the overloaded core to the underloaded core
                    task = (
                        overloaded_core.ready_queue.pop()
                    )  # Take the last task from the ready queue
                    underloaded_core.assign_task(task)
                    task.state = Task_State.READY  # Update the task state
                    self.file.write(
                        f"{task.name} migrated from Core {overloaded_core.id} to Core {underloaded_core.id}\n"
                    )
                    break  # Move to the next underloaded core after transferring one task

    def execute(self):
        for core in self.cores:
            core.execute()

        if self.time % 4 == 0:
            self.load_balancing()

        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.select_core(task)
                core.assign_task(task)
                self.waiting_queue.remove(task)

    def add_task(self, task):
        if self.allocate_resources(task):
            core = self.select_core(task)
            core.assign_task(task)
        else:
            self.waiting_queue.append(task)
            task.state = Task_State.WAITING

    def select_core(self, task):
        return self.cores[task.destination_CPU_number - 1]


class Subsystem_2(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.cores = [Core_2(i, self) for i in range(num_cores)]

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self):
        for core in self.cores:
            core.execute()

    def add_task(self, task):
        # Add a task to the ready queue
        task.state = Task_State.READY
        heapq.heappush(self.ready_queue, task)

        # Assign task to core
        assigned = False
        for core in self.cores:
            if self.ready_queue:
                if core.current_task is None:
                    core.assign_task()
                    assigned = True
                    break
        if not assigned:
            for core in self.cores:
                if self.ready_queue:
                    if core.current_task.remaining_time > task.remaining_time:
                        core.assign_task()
                        break

        # Deadlock detection
        count = 0
        for core in self.cores:
            if core.current_task is not None:
                if not core.current_task.has_all_resources:
                    count += 1

        if count == 2:  # Deadlock has occurred.
            self.file.write(f"Deadlock has occurred !!!!!\n")

            # Deadlock resolution
            for task in self.ready_queue:
                self.release_resources(task)
                task.has_all_resources = False
                task.remaining_time = task.execution_time


class Subsystem_3(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_3(i, self) for i in range(num_cores)]

        self.is_schedulable = None
        self.hyper_period = None

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue {[task.name for task in self.waiting_queue]}\n"
        )
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}"
            status += f", number of repeat times: {core.current_task.number_of_repeat_times if core.current_task else '-'}\n"
            status += f"                Ready Queue: {[task.name for task in core.ready_queue]}\n"
        return status

    def hyperperiod(self):
        temp = []
        for task in self.ready_queue:
            temp.append(task.period)
        hp = temp[0]
        for i in temp[1:]:
            hp = hp * i // gcd(hp, i)
        # print("Hyperperiod:", hp)
        return hp

    def schedulablity(self):
        """
        Calculates the utilization factor of the tasks to be scheduled
        and then checks for the schedulablity and then returns true is
        schedulable else false.
        """

        T = []
        C = []
        U = []
        n = len(self.ready_queue)

        for i in range(n):
            T.append(self.ready_queue[i].period)
            C.append(self.ready_queue[i].execution_time)
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

    def check_validation(self):
        for task in self.ready_queue:
            if task.execution_time > task.period:
                print(f"{task.name} can not be completed in the specified time !")

    def give_next_task(self):
        priority_task = None
        min_period = float("inf")

        for task in self.ready_queue:
            if task.remaining_time - 1 != 0:  # Task is ready
                if task.period < min_period:
                    min_period = task.period
                    priority_task = task

        return priority_task

    def add_task(self, task):
        task.state = Task_State.READY
        self.ready_queue.append(task)

    def execute(self):
        if self.time == 0:
            self.is_schedulable = self.schedulablity()
            if self.is_schedulable:
                self.hyper_period = self.hyperperiod()
                self.check_validation()

        priority_task = self.give_next_task()
        self.cores[0].assign_task(priority_task)
        self.cores[0].execute()

        # Update Period after each clock cycle
        for task in self.ready_queue:
            task.period -= 1
            if task.period == 0:
                task.remaining_time = task.execution_time + 1
                task.period = task.backup_period
                task.number_of_repeat_times -= 1
                if task.number_of_repeat_times == 0:
                    self.ready_queue.remove(task)

        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.select_core(task)
                core.assign_task(task)
                self.waiting_queue.remove(task)

    def drawGantt(self):
        """
        The scheduled results are displayed in the form of a
        gantt chart for the user to get better understanding
        """
        n = len(self.ready_queue)
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


class Subsystem_4(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.completed_tasks = []
        self.cores = [Core_4(i, self) for i in range(num_cores)]

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += (
            f"        Waiting Queue: {[task.name for task in self.waiting_queue]}\n"
        )
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"
        return status

    def execute(self):

        # Moving tasks from waiting queue to ready queue
        if self.waiting_queue:
            for _ in self.waiting_queue:
                task = self.waiting_queue.pop(0)
                for completed_task in self.completed_tasks:
                    if task.prerequisite_task_name == completed_task.name:
                        task.prerequisite = True
                        break
                if task.prerequisite:
                    if self.allocate_resources(task):
                        task.arrival_time = self.time
                        self.ready_queue.append(task)
                    else:
                        self.waiting_queue.append(task)
                else:
                    self.waiting_queue.append(task)

        # Assign task to core
        for core in self.cores:
            if self.ready_queue:
                if core.current_task is None:
                    core.assign_task()
                    break

        for core in self.cores:
            core.execute()

    def add_task(self, task):
        # For prerequisite tasks
        if task.prerequisite_task_name == "-":
            task.prerequisite = True
        else:
            for completed_task in self.completed_tasks:
                if task.prerequisite_task_name == completed_task.name:
                    task.prerequisite = True
                    break

        # Append to the waiting queue or ready queue
        if task.prerequisite:
            if self.allocate_resources(task):
                task.state = Task_State.READY
                self.ready_queue.append(task)
                self.file.write(f"Task [{task.name}] appended to ready queue !\n")
            else:
                task.state = Task_State.WAITING
                self.waiting_queue.append(task)
                self.file.write(f"Task [{task.name}] appended to waiting queue !\n")
        else:
            task.state = Task_State.WAITING
            self.waiting_queue.append(task)
            self.file.write(f"Task [{task.name}] appended to waiting queue !\n")
