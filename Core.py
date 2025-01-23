# from sys import *
import heapq
import random
from Task import *


# For gantt chart
y_axis = []
from_x = []
to_x = []


class Core:
    def __init__(self, id, subsystem):
        self.id = id + 1
        self.subsystem = subsystem
        self.current_task = None

    def assign_task(self, task):
        if self.current_task is None:
            self.current_task = task
            task.state = Task_State.RUNNING
        else:
            heapq.heappush(self.ready_queue, task)
            task.state = Task_State.READY

    def execute(self):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = Task_State.READY
                self.current_task = None
                if self.ready_queue:
                    next_task = heapq.heappop(self.ready_queue)
                    self.assign_task(next_task)


class Core_1(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)
        self.ready_queue = []
        self.min_execution_time = None

    def assign_task(self, task):
        self.set_a_task_quantum(task)
        if self.current_task is None:
            task.state = Task_State.RUNNING
            self.current_task = task
        else:
            task.state = Task_State.READY
            self.ready_queue.append(task)

    def determine_min_execution_time(self):
        if self.current_task is None:
            min_execution_time = 1000
        else:
            min_execution_time = self.current_task.execution_time

        for task in self.ready_queue:
            if task.execution_time < min_execution_time:
                min_execution_time = task.execution_time
        self.min_execution_time = min_execution_time

    def set_a_task_quantum(self, task):
        if task.remaining_quantum == 0 and self.min_execution_time is not None:
            task.remaining_quantum = (
                task.execution_time // self.min_execution_time
            ) + 1
            if task.remaining_quantum == 1:
                task.remaining_quantum += 1
            self.subsystem.file.write(
                f"{task.name} remaining quantum: {task.remaining_quantum}\n"
            )

    def set_all_tasks_quantums(self):
        if self.current_task is not None:
            task = self.current_task
            task.remaining_quantum = task.execution_time // self.min_execution_time
            task.remaining_quantum += 1
            self.subsystem.file.write(
                f"{task.name} remaining_quantum = {task.remaining_quantum}\n"
            )
        for task in self.ready_queue:
            task.remaining_quantum = task.execution_time // self.min_execution_time
            task.remaining_quantum += 1
            self.subsystem.file.write(
                f"{task.name} remaining_quantum = {task.remaining_quantum}\n"
            )

    def execute(self):
        if self.subsystem.time % 10 == 0:
            self.determine_min_execution_time()
            self.subsystem.file.write(
                f"Core: {self.id} min execution time: {self.min_execution_time}\n"
            )
            self.set_all_tasks_quantums()

        if self.current_task is not None:
            if self.subsystem.time - self.current_task.arrival_time != 0:
                self.current_task.remaining_time -= 1
                self.current_task.remaining_quantum -= 1

                if self.current_task.remaining_time == 0:
                    self.current_task.state = Task_State.COMPLETED
                    self.subsystem.release_resources(self.current_task)

                    self.current_task = None
                    if self.ready_queue:
                        next_task = self.ready_queue.pop(0)
                        self.assign_task(next_task)

                elif self.current_task.remaining_quantum == 0:
                    self.subsystem.file.write(
                        f"Core: {self.id}, {self.current_task.name} remaining quantum: 0 --> "
                    )
                    self.current_task.state = Task_State.READY
                    self.set_a_task_quantum(self.current_task)
                    self.ready_queue.append(self.current_task)

                    self.current_task = None
                    if self.ready_queue:
                        next_task = self.ready_queue.pop(0)
                        self.assign_task(next_task)


class Core_2(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)
        self.ready_queue = subsystem.ready_queue

    def assign_task(self):
        task = heapq.heappop(self.ready_queue)
        if not task.has_all_resources:
            if self.subsystem.allocate_resources(task):
                self.subsystem.file.write(
                    f"Resources allocated to task [{task.name}] !\n"
                )
            else:
                self.subsystem.file.write(
                    f"Resources were not allocated to task [{task.name}] !\n"
                )
        if self.current_task is None:
            self.current_task = task
            self.current_task.state = Task_State.RUNNING
        else:
            self.current_task.state = Task_State.READY
            self.subsystem.file.write(f"Task [{self.current_task.name}] preemped !\n")
            heapq.heappush(self.ready_queue, self.current_task)
            self.current_task = task
            self.current_task.state = Task_State.RUNNING
            self.subsystem.file.write(
                f"Task [{self.current_task.name}] assigned to CPU !\n"
            )

    def execute(self):
        if self.current_task is not None:
            if (
                self.subsystem.time - self.current_task.arrival_time != 0
                and self.current_task.has_all_resources
            ):
                self.current_task.remaining_time -= 1

            if self.current_task.remaining_time == 0:  # Task completed
                self.current_task.state = Task_State.COMPLETED
                self.subsystem.release_resources(self.current_task)
                self.subsystem.file.write(
                    f"Task [{self.current_task.name}] completed !\n"
                )

                # Assign new task to core
                self.current_task = None
                if len(self.ready_queue) > 0:
                    self.assign_task()

            if (
                self.current_task is not None
                and not self.current_task.has_all_resources
            ):
                self.subsystem.allocate_resources(self.current_task)


class Core_3(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)
        self.ready_queue = subsystem.ready_queue

    def assign_task(self, task):
        if task is not None:
            task.state = Task_State.RUNNING
        self.current_task = task

    def execute(self):
        t = self.subsystem.time
        from_x.append(t)
        to_x.append(t + 1)

        if self.current_task is not None:  # core is not idle
            y_axis.append(f"{self.current_task.name}")
            self.current_task.remaining_time -= 1
        else:  # core is idle
            y_axis.append("IDLE")


class Core_4(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)

    def assign_task(self):
        if self.subsystem.ready_queue:
            task = self.subsystem.ready_queue.pop(0)
            self.current_task = task
            self.current_task.state = Task_State.RUNNING

    def execute(self):
        if self.current_task is not None:
            if self.subsystem.time - self.current_task.arrival_time != 0:
                self.current_task.remaining_time -= 1

                # For an error with a probability of 30 percent
                random_number = random.random()
                if random_number < 0.3:
                    self.current_task.remaining_time += 1
                    self.subsystem.file.write(
                        f"Task [{self.current_task.name}] failed !\n"
                    )

            if self.current_task.remaining_time == 0:  # Task completed
                self.current_task.state = Task_State.COMPLETED
                self.subsystem.completed_tasks.append(self.current_task)
                self.subsystem.release_resources(self.current_task)
                self.subsystem.file.write(
                    f"Task [{self.current_task.name}] completed !\n"
                )
                self.current_task = None
