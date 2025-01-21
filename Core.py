import heapq
from Task import *


class Core:
    def __init__(self, core_id, subsystem):
        self.core_id = core_id
        self.subsystem = subsystem
        self.current_task = None

    def assign_task(self, task):
        if self.current_task is None:
            self.current_task = task
            task.state = Task_State.RUNNING
        else:
            heapq.heappush(self.ready_queue, task)
            task.state = Task_State.READY

    def execute(self, time):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = Task_State.READY
                self.current_task = None
                if self.ready_queue:
                    next_task = heapq.heappop(self.ready_queue)
                    self.assign_task(next_task)


class Core_1(Core):
    def __init__(self, core_id, subsystem):
        super().__init__(core_id, subsystem)
        self.ready_queue = []
        self.min_execution_time = None

    def assign_task(self, task):
        if task.remaining_quantum is None and self.min_execution_time is not None:
            if self.min_execution_time == float("inf"):
                task.remaining_quantum = 1
            else:
                task.remaining_quantum = task.execution_time // self.min_execution_time
            print(
                f"::: {task.name}, q: {task.remaining_quantum}, min_execution_time: {self.min_execution_time}"
            )

        if self.current_task is None:
            task.state = Task_State.RUNNING
            self.current_task = task
        else:
            task.state = Task_State.READY
            self.ready_queue.append(task)

    def determine_min_execution_time(self):
        if self.current_task is None:
            min_execution_time = float("inf")
        else:
            min_execution_time = self.current_task.execution_time

        for task in self.ready_queue:
            if task.execution_time < min_execution_time:
                min_execution_time = task.execution_time
        self.min_execution_time = min_execution_time

    def set_tasks_quantum(self):
        if self.current_task is not None:
            task = self.current_task
            task.remaining_quantum = task.execution_time // self.min_execution_time
            print(f"{task.name} remaining_quantum = {task.remaining_quantum}")
        for task in self.ready_queue:
            task.remaining_quantum = task.execution_time // self.min_execution_time
            print(f"{task.name} remaining_quantum = {task.remaining_quantum}")

    def execute(self, time):
        if time % 5 == 0:
            self.determine_min_execution_time()
            print(f"\nTime: {time}")
            print(f"min execution time: {self.min_execution_time}")
            self.set_tasks_quantum()

        if self.current_task is not None:
            if time - self.current_task.arrival_time != 0:
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
                    self.current_task.state = Task_State.READY
                    if self.min_execution_time == float("inf"):
                        self.current_task.remaining_quantum = 1
                    else:
                        self.current_task.remaining_quantum = (
                            self.current_task.execution_time // self.min_execution_time
                        )
                    self.ready_queue.append(self.current_task)

                    self.current_task = None
                    if self.ready_queue:
                        next_task = self.ready_queue.pop(0)
                        self.assign_task(next_task)


class Core_2(Core):
    def __init__(self, core_id, subsystem):
        super().__init__(core_id, subsystem)
        self.ready_queue = subsystem.ready_queue

    def assign_task(self):
        if self.current_task is None:
            self.current_task = heapq.heappop(self.ready_queue)
            self.current_task.state = Task_State.RUNNING
        else:
            print(f"Task {self.current_task.name} preemped")
            self.current_task.state = Task_State.READY
            heapq.heappush(self.ready_queue, self.current_task)
            self.current_task = heapq.heappop(self.ready_queue)
            self.current_task.state = Task_State.RUNNING
            print(f"Task {self.current_task.name} assigned to CPU")

    def execute(self, time):
        if self.current_task is not None:
            self.current_task.remaining_time -= 1
            if self.current_task.remaining_time == 0:
                self.current_task.state = (
                    Task_State.READY
                )  # this has to be COMPLETED not READY
                self.current_task = None
                if len(self.ready_queue) > 0:
                    self.assign_task()


class Core_3(Core):
    def __init__(self, core_id, subsystem):
        super().__init__(core_id, subsystem)
        self.ready_queue = []


class Core_4(Core):
    def __init__(self, core_id, subsystem):
        super().__init__(core_id, subsystem)
        self.ready_queue = subsystem.ready_queue
