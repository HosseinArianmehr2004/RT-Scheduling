import heapq
import threading
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

    def draw_gantt_chart(self, core):
        """
        The scheduled results are displayed in the form of a
        gantt chart for the user to get better understanding
        """
        index = int(self.id.split("_")[1])
        colors = ["red", "green", "blue", "yellow"]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # the data is plotted from_x to to_x along y_axis
        ax = plt.hlines(
            core.y_axis,
            core.from_x,
            core.to_x,
            linewidth=20,
            color=colors[index - 1],
        )
        plt.title(f"{self.id} Core_{core.id}")
        plt.grid(True)
        plt.xlabel("Real-Time clock")
        if self.id == "Subsystem_3":
            plt.ylabel("HIGH ----------------- Priority --------------------> LOW")
        else:
            plt.ylabel("<------------------ Tasks ------------------>")

        plt.xticks(np.arange(min(core.from_x), max(core.to_x) + 1, 1.0))

        # plt.show()

        plt.savefig(f"figures/{self.id}_Core_{core.id}.png", bbox_inches="tight")
        # plt.close(fig)  # Close the figure to free up memory


class Subsystem_1(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_1(i, self) for i in range(num_cores)]

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

            t = self.time
            core.from_x.append(t)
            core.to_x.append(t + 1)

            if core.current_task is not None:  # core is not idle
                core.y_axis.append(f"{core.current_task.name}")
            else:  # core is idle
                core.y_axis.append("IDLE")

        return status

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

    def select_core(self, task):
        return self.cores[task.destination_CPU_number - 1]

    def set_all_tasks_quantums(self, core):
        if core.current_task is not None:
            task = core.current_task
            task.remaining_quantum = task.execution_time // core.min_execution_time
            task.remaining_quantum += 1
            self.file.write(
                f"{task.name} remaining_quantum = {task.remaining_quantum}\n"
            )
        for task in core.ready_queue:
            task.remaining_quantum = task.execution_time // core.min_execution_time
            task.remaining_quantum += 1
            self.file.write(
                f"{task.name} remaining_quantum = {task.remaining_quantum}\n"
            )

    def determine_min_execution_time(self, core):
        if core.current_task is None:
            min_execution_time = 1000
        else:
            min_execution_time = core.current_task.execution_time

        for task in core.ready_queue:
            if task.execution_time < min_execution_time:
                min_execution_time = task.execution_time

        core.min_execution_time = min_execution_time

    def set_task_quantum(self, task, core):
        if task.remaining_quantum == 0 and core.min_execution_time is not None:
            task.remaining_quantum = (
                task.execution_time // core.min_execution_time
            ) + 1
            if task.remaining_quantum == 1:
                task.remaining_quantum += 1
            self.file.write(
                f"{task.name} remaining quantum: {task.remaining_quantum}\n"
            )

    def add_task(self, task):
        if self.allocate_resources(task):
            core = self.select_core(task)
            self.set_task_quantum(task, core)
            core.assign_task(task)
        else:
            self.waiting_queue.append(task)
            task.state = Task_State.WAITING

    def execute(self):
        # determine mi execution time of all the tasks in each cores ready queue
        if self.time % 10 == 0:
            for core in self.cores:
                self.determine_min_execution_time(core)
                self.file.write(
                    f"Core: {core.id} min execution time: {core.min_execution_time}\n"
                )
                self.set_all_tasks_quantums(core)

        for core in self.cores:
            core.execute()

            if core.current_task is not None:
                if core.current_task.remaining_time == 0:
                    core.current_task.state = Task_State.COMPLETED
                    self.release_resources(core.current_task)

                    core.current_task = None
                    if core.ready_queue:
                        next_task = core.ready_queue.pop(0)
                        core.assign_task(next_task)

                elif core.current_task.remaining_quantum == 0:
                    self.file.write(
                        f"Core: {core.id}, {core.current_task.name} remaining quantum: 0 --> "
                    )
                    core.current_task.state = Task_State.READY
                    self.set_task_quantum(core.current_task, core)
                    core.ready_queue.append(core.current_task)

                    core.current_task = None
                    if core.ready_queue:
                        next_task = core.ready_queue.pop(0)
                        core.assign_task(next_task)

        if self.time % 4 == 0:
            self.load_balancing()

        # Check waiting queue and try to assign tasks
        for task in self.waiting_queue[:]:
            if self.allocate_resources(task):
                core = self.select_core(task)
                core.assign_task(task)
                self.waiting_queue.remove(task)

    def draw_gantt_chart(self):
        for core in self.cores:
            super().draw_gantt_chart(core)


class Subsystem_2(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.cores = [Core_2(i, self) for i in range(num_cores)]
        self.lock = threading.Lock()

    def get_status(self):
        status = f"Sub{self.id}:\n"
        status += f"        Resources: R1: {self.resources['R1'].available_units} R2: {self.resources['R2'].available_units}\n"
        status += f"        Ready Queue: {[task.name for task in self.ready_queue]}\n"
        for core in self.cores:
            status += f"        Core{core.id}:\n"
            status += f"                Running Task: {core.current_task.name if core.current_task else '---'}"
            status += f", remaining time: {core.current_task.remaining_time if core.current_task else '-'}\n"

            t = self.time
            core.from_x.append(t)
            core.to_x.append(t + 1)

            if core.current_task is not None:  # core is not idle
                core.y_axis.append(f"{core.current_task.name}")
            else:  # core is idle
                core.y_axis.append("IDLE")

        return status

    def execute(self):
        # Execute with thread
        threads = []
        for core in self.cores:
            thread = threading.Thread(target=core.execute)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def add_task(self, task):
        # Add a task to the ready queue
        task.state = Task_State.READY
        heapq.heappush(self.ready_queue, task)

        # Assign task to cores
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
            with self.lock:
                self.file.write(f"Deadlock has occurred !!!!!\n")

            # Deadlock resolution
            for task in self.ready_queue:
                self.release_resources(task)
                task.has_all_resources = False
                task.remaining_time = task.execution_time

    def draw_gantt_chart(self):
        for core in self.cores:
            super().draw_gantt_chart(core)


class Subsystem_3(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.cores = [Core_3(i, self) for i in range(num_cores)]
        self.lock = threading.Lock()

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
                    count += 1

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
            if task.remaining_time != 0:  # Task is ready
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

        # Execute with thread
        threads = []
        for core in self.cores:
            thread = threading.Thread(target=core.execute)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Update Period after each clock cycle
        for task in self.ready_queue:
            task.period -= 1
            if task.period == 0:
                task.remaining_time = task.execution_time
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

    def draw_gantt_chart(self):
        for core in self.cores:
            super().draw_gantt_chart(core)


class Subsystem_4(Subsystem):
    def __init__(self, id, num_cores, resources):
        super().__init__(id, resources)
        self.waiting_queue = []
        self.completed_tasks = []
        self.cores = [Core_4(i, self) for i in range(num_cores)]
        self.lock = threading.Lock()

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

            t = self.time
            core.from_x.append(t)
            core.to_x.append(t + 1)

            if core.current_task is not None:  # core is not idle
                core.y_axis.append(f"{core.current_task.name}")
            else:  # core is idle
                core.y_axis.append("IDLE")

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

        # Assign task to cores
        for core in self.cores:
            if self.ready_queue:
                if core.current_task is None:
                    core.assign_task()
                    break

        # Execute with thread
        threads = []
        for core in self.cores:
            thread = threading.Thread(target=core.execute)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

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
                with self.lock:
                    self.file.write(f"Task [{task.name}] appended to ready queue !\n")
            else:
                task.state = Task_State.WAITING
                self.waiting_queue.append(task)
                with self.lock:
                    self.file.write(f"Task [{task.name}] appended to waiting queue !\n")
        else:
            task.state = Task_State.WAITING
            self.waiting_queue.append(task)
            with self.lock:
                self.file.write(f"Task [{task.name}] appended to waiting queue !\n")

    def draw_gantt_chart(self):
        for core in self.cores:
            super().draw_gantt_chart(core)
