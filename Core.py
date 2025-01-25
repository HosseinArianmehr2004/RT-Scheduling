import heapq
import threading
import random
from Task import *


class Core:
    def __init__(self, id, subsystem):
        self.id = id + 1
        self.subsystem = subsystem
        self.current_task = None

        # For gantt chart
        self.y_axis = []
        self.from_x = []
        self.to_x = []

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
        if self.current_task is None:
            task.state = Task_State.RUNNING
            self.current_task = task
        else:
            task.state = Task_State.READY
            self.ready_queue.append(task)

    def execute(self):
        if self.current_task is not None:
            if self.subsystem.time - self.current_task.arrival_time != 0:
                if not self.current_task.start_time_bool:
                    self.current_task.start_execution_time = self.subsystem.time - 1
                    self.current_task.start_time_bool = True

                self.current_task.remaining_time -= 1
                self.current_task.remaining_quantum -= 1

            execution_core = False
            if self.current_task.execution_cores:
                for core in self.current_task.execution_cores:
                    if self.id == core:
                        execution_core = True
                        break
            if not execution_core:
                self.current_task.execution_cores.append(self.id)


class Core_2(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)
        self.ready_queue = subsystem.ready_queue
        self.lock = threading.Lock()

    def assign_task(self):
        task = heapq.heappop(self.ready_queue)
        if not task.has_all_resources:
            if self.subsystem.allocate_resources(task):
                with self.lock:
                    self.subsystem.file.write(
                        f"Resources allocated to task [{task.name}] !\n"
                    )
            else:
                with self.lock:
                    self.subsystem.file.write(
                        f"Resources were not allocated to task [{task.name}] !\n"
                    )
        if self.current_task is None:
            self.current_task = task
            self.current_task.state = Task_State.RUNNING
        else:
            self.current_task.state = Task_State.READY
            with self.lock:
                self.subsystem.file.write(
                    f"Task [{self.current_task.name}] preempted !\n"
                )
            heapq.heappush(self.ready_queue, self.current_task)
            self.current_task = task
            self.current_task.state = Task_State.RUNNING
            with self.lock:
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

            if (
                self.current_task.execution_time == self.current_task.remaining_time
                and not self.current_task.start_time_bool
            ):
                self.current_task.start_execution_time = self.subsystem.time
                self.current_task.start_time_bool = True

            execution_core = False
            if self.current_task.execution_cores:
                for core in self.current_task.execution_cores:
                    if self.id == core:
                        execution_core = True
                        break
            if not execution_core:
                self.current_task.execution_cores.append(self.id)

            if self.current_task.remaining_time == 0:  # Task completed
                self.current_task.state = Task_State.COMPLETED
                self.subsystem.release_resources(self.current_task)
                self.current_task.finish_execution_time = self.subsystem.time
                with self.lock:
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
        self.from_x.append(t)
        self.to_x.append(t + 1)

        if self.current_task is not None:  # core is not idle
            self.y_axis.append(f"{self.current_task.name}")
            if (
                self.current_task.execution_time == self.current_task.remaining_time
                and not self.current_task.start_time_bool
            ):
                self.current_task.start_execution_time = self.subsystem.time
                self.current_task.start_time_bool = True

            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.number_of_repeat_times -= 1

            execution_core = False
            if self.current_task.execution_cores:
                for core in self.current_task.execution_cores:
                    if self.id == core:
                        execution_core = True
                        break
            if not execution_core:
                self.current_task.execution_cores.append(self.id)
        else:  # core is idle
            self.y_axis.append("IDLE")


class Core_4(Core):
    def __init__(self, id, subsystem):
        super().__init__(id, subsystem)
        self.ready_queue = subsystem.ready_queue

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
                    with self.subsystem.lock:
                        self.subsystem.file.write(
                            f"Task [{self.current_task.name}] failed !\n"
                        )

            if (
                self.current_task.execution_time == self.current_task.remaining_time
                and not self.current_task.start_time_bool
            ):
                self.current_task.start_execution_time = self.subsystem.time
                self.current_task.start_time_bool = True

            execution_core = False
            if self.current_task.execution_cores:
                for core in self.current_task.execution_cores:
                    if self.id == core:
                        execution_core = True
                        break
            if not execution_core:
                self.current_task.execution_cores.append(self.id)

            if self.current_task.remaining_time == 0:  # Task completed
                self.current_task.state = Task_State.COMPLETED
                self.subsystem.completed_tasks.append(self.current_task)
                self.subsystem.release_resources(self.current_task)
                self.current_task.finish_execution_time = self.subsystem.time
                with self.subsystem.lock:
                    self.subsystem.file.write(
                        f"Task [{self.current_task.name}] completed !\n"
                    )
                self.current_task = None
